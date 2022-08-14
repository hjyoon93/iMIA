package edu.gmu.c4i.dalnim.util;

import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.lang.reflect.Method;
import java.net.URI;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;
import java.util.Properties;

import org.apache.commons.lang3.StringUtils;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * Loads application.properties from working directory.
 * 
 * @author Shou Matsumoto
 */
public class ApplicationProperties extends Properties {

	private static final long serialVersionUID = -997452461515236855L;

	private static final ApplicationProperties SINGLETON = new ApplicationProperties();

	private static Logger logger = LoggerFactory.getLogger(ApplicationProperties.class);

	/**
	 * Objects must be accessed via {@link #getInstance()}
	 */
	private ApplicationProperties() {
		try {
			loadFile();
		} catch (Exception e) {
			logger.warn("No application.properties loaded from path '{}'. ",
					getClass().getClassLoader().getResource("/"), e);
		}
	}

	/**
	 * @return a singleton property object.
	 */
	public static ApplicationProperties getInstance() {
		return SINGLETON;
	}

	/**
	 * Loads the content of application.properties file.
	 * 
	 * @throws IOException
	 */
	protected void loadFile() throws IOException {

		// loadFile is called in constructor (while logger is not initialized).
		// Use own logger if logger is not ready.
		Logger log = logger;
		if (log == null) {
			// eager load logger to make sure next loadFile will use it
			log = LoggerFactory.getLogger(ApplicationProperties.class);
		}

		URI resource = null;
		List<Exception> exceptions = new ArrayList<>(2);

		try {
			log.info("Attempting to load application.properties from classloader's root '{}'",
					getClass().getClassLoader().getResource("."));
			resource = getClass().getClassLoader().getResource("application.properties").toURI();
		} catch (Exception e) {
			exceptions.add(e);
			log.info("Could not load application.properties from classloader's root. Retrying different location...");
		}
		if (resource == null) {
			try {
				log.info("Attempting to load application.properties from working directory '{}'",
						Path.of(".").toAbsolutePath());
				resource = new File("application.properties").getAbsoluteFile().toURI();
			} catch (Exception e) {
				exceptions.add(e);
				log.info("Could not load application.properties from working directory.");
			}
		}
		if (resource != null) {
			try {
				log.info("Loading application.properties from '{}'", resource);
				this.load(new FileInputStream(new File(resource)));
				return;
			} catch (Exception e) {
				exceptions.add(e);
				log.warn("Failed to load application properties from '{}'. Ignoring...", resource);
			}
		}

		// if reached this point, all attempts have failed
		for (int i = 0; i < exceptions.size(); i++) {
			log.warn("Exception {}:", (i + 1), exceptions.get(i));
		}
		log.warn("The application.properties was not found. Ignoring...");
	}

	/**
	 * Load some attributes from application.properties and injects them to class
	 * variables/attributes by using reflection, but only string types are allowed.
	 * 
	 * @param obj : the object to inject the loaded attributes
	 */
	public void loadApplicationProperties(Object obj) {

		if (obj == null) {
			logger.warn("No object was specified when loading and injecting applications.properties. Ignoring...");
			return;
		}

		Class<? extends Object> clazz = obj.getClass();

		this.entrySet().stream()
				// key is in the format <CLASS>.<ATTRIBUTE NAME>.
				// Only consider keys with same class name.
				.filter(entry -> entry.getKey().toString().startsWith(clazz.getName()))
				// Inject attribute values
				.forEach(entry -> {
					try {
						logger.debug("Processing property {}", entry);

						// Extract <ATTRIBUTE NAME>
						String attributeName = entry.getKey().toString().substring(clazz.getName().length()
								// +1 to ignore "."
								+ 1);
						logger.debug("Attribute name = {}", attributeName);

						// use reflection to set
						// assume string argument by default
						Method setter = clazz.getMethod("set" + StringUtils.capitalize(attributeName), String.class);
						logger.debug("Setter = {}", setter);

						setter.invoke(obj, entry.getValue().toString());
					} catch (Exception e) {
						logger.warn("Failed to handle property {}", entry, e);
					}
				});
	}

}
