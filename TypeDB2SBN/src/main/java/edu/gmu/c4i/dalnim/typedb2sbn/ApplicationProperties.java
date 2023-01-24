package edu.gmu.c4i.dalnim.typedb2sbn;

import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.lang.reflect.Method;
import java.net.URI;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;
import java.util.Optional;
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

		for (java.util.Map.Entry<Object, Object> entry : this.entrySet()) {
			if (!entry.getKey().toString().startsWith(clazz.getName())) {
				continue;
			}
			try {
				logger.debug("Processing property {}", entry);

				// Extract <ATTRIBUTE NAME>
				String attributeName = entry.getKey().toString().substring(clazz.getName().length()
						// +1 to ignore "."
						+ 1);
				logger.debug("Attribute name = {}", attributeName);

				// use reflection to set
				Method setter = getMethodByName(clazz, "set" + StringUtils.capitalize(attributeName)).orElseThrow();
				logger.debug("Setter = {}", setter);

				// check the type of the parameter
				Class<?> paramClass = setter.getParameterTypes()[0];

				// handle numbers and booleans
				if (paramClass.isAssignableFrom(int.class)) {
					setter.invoke(obj, Integer.parseInt(entry.getValue().toString()));
					logger.debug("Assigned an int parameter to setter {}", setter);
				} else if (paramClass.isAssignableFrom(Integer.class)) {
					setter.invoke(obj, Integer.valueOf(entry.getValue().toString()));
					logger.debug("Assigned an Integer parameter to setter {}", setter);
				} else if (paramClass.isAssignableFrom(long.class)) {
					setter.invoke(obj, Long.parseLong(entry.getValue().toString()));
					logger.debug("Assigned long parameter to setter {}", setter);
				} else if (paramClass.isAssignableFrom(Long.class)) {
					setter.invoke(obj, Long.valueOf(entry.getValue().toString()));
					logger.debug("Assigned Long parameter to setter {}", setter);
				} else if (paramClass.isAssignableFrom(float.class)) {
					setter.invoke(obj, Float.parseFloat(entry.getValue().toString()));
					logger.debug("Assigned float parameter to setter {}", setter);
				} else if (paramClass.isAssignableFrom(Float.class)) {
					setter.invoke(obj, Float.valueOf(entry.getValue().toString()));
					logger.debug("Assigned Float parameter to setter {}", setter);
				} else if (paramClass.isAssignableFrom(double.class)) {
					setter.invoke(obj, Double.parseDouble(entry.getValue().toString()));
					logger.debug("Assigned double parameter to setter {}", setter);
				} else if (paramClass.isAssignableFrom(Double.class)) {
					setter.invoke(obj, Double.valueOf(entry.getValue().toString()));
					logger.debug("Assigned Double parameter to setter {}", setter);
				} else if (paramClass.isAssignableFrom(boolean.class)) {
					setter.invoke(obj, Boolean.parseBoolean(entry.getValue().toString()));
					logger.debug("Assigned boolean parameter to setter {}", setter);
				} else if (paramClass.isAssignableFrom(Boolean.class)) {
					setter.invoke(obj, Boolean.valueOf(entry.getValue().toString()));
					logger.debug("Assigned Boolean parameter to setter {}", setter);
				} else {
					// use string as default...
					setter.invoke(obj, entry.getValue().toString());
					logger.debug("Assigned a String parameter to setter {}", setter);
				}
			} catch (Exception e) {
				logger.warn("Failed to handle property {}", entry, e);
			}

		}
	}

	/**
	 * Search for a method with the provided name.
	 * 
	 * @param clazz : class to search for method
	 * @param name  : method's name
	 * @return the method object obtained with reflection.
	 */
	protected Optional<Method> getMethodByName(Class<? extends Object> clazz, String name) {
		if (clazz == null || name == null) {
			return Optional.empty();
		}

		for (Method method : clazz.getMethods()) {
			if (method.getName().equals(name)) {
				return Optional.of(method);
			}
		}

		return Optional.empty();
	}

}
