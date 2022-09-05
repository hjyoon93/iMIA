# Release notes

## 0.0.4

- Added support for tags which are sensitive to position/ordering, such as the *waypoint* tag. *BPMNattrib_sort* attribute will store their positions.

- Added semantic mappings to DALNIM concept model. It can be enabled from the application.properties by setting edu.gmu.c4i.dalnim.bpmn2typedb.encoder.EncoderImpl.mapBPMNToConceptualModel=true.

## 0.0.3

- Added support for BPMN data references.

## 0.0.2

- Substituted Resource with Asset in conceptual model.

- Updated some typeql rules to reflect the above change.

- Bugfixes and instrumentation.
 
## 0.0.1

- Initial release
