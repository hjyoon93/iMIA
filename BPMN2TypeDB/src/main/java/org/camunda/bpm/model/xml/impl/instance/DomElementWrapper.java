package org.camunda.bpm.model.xml.impl.instance;

import java.util.Optional;

import org.camunda.bpm.model.xml.instance.DomElement;
import org.w3c.dom.Element;

/**
 * Adapter/wrapper class for {@link DomElementImpl} used in
 * {@link edu.gmu.c4i.dalnim.bpmn2typedb.encoder.EncoderImpl} to expose a XML
 * DOM element.
 * 
 * @author shou
 */
public class DomElementWrapper extends DomElementImpl {

	private DomElementImpl wrapped;

	/**
	 * Protected to avoid public access. Use {@link #wrap(DomElement)} instead.
	 * 
	 * @see #wrap(DomElement)
	 */
	protected DomElementWrapper(DomElementImpl wrapped) {
		super(wrapped.getElement());
		this.wrapped = wrapped;
	}

	public static DomElementWrapper wrap(DomElement domElement) {
		if (domElement instanceof DomElementImpl) {
			return new DomElementWrapper(((DomElementImpl) domElement));
		}
		throw new IllegalArgumentException("Current implementation only supports instances of " + DomElementImpl.class);
	}

	/**
	 * Makes {@link #getElement()} visible publicly.
	 * 
	 * @return the {@link #getElement()}
	 */
	public Optional<Element> getOriginalElement() {
		DomElementImpl dom = getWrapped();
		if (dom == null) {
			return Optional.empty();
		}
		return Optional.ofNullable(dom.getElement());
	}

	/**
	 * @return the wrapped object.
	 */
	public DomElementImpl getWrapped() {
		return wrapped;
	}

	/**
	 * @param wrapped : the wrapped object to set
	 */
	public void setWrapped(DomElementImpl wrapped) {
		this.wrapped = wrapped;
	}
}
