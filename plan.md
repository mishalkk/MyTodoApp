# Questions for the professor: pseudonymized machine data

## Current status

The main dataset scope is established. Exact measurements depend on thesis agreement and receipt of the full raw data. Raw signal delivery still needs to be reconciled with the professor's request.

## Current answers for the professor

1. **Data for each pseudonymized machine:** Both machines have the same set of 300+ sensor attributes, including numerical, categorical, and binary values. Machine ID is the only fixed attribute identified so far. Internal attribute names will be replaced with generic descriptive names that retain the sensor's meaning. The deliverable is an event-level classification dataset, with one row per stop containing aggregated sensor features and a stop-type label. The provisional source window is 7 seconds before and 3 seconds after each stop. Raw signal series will not be delivered; the derivation will be documented in detail. Exact attribute ranges, possible categorical/binary values, sampling interval, and readings per window can be determined after full data access.
2. **Number of machines:** Two, covering six months of operation each. Raw data is approximately 100+ GB per machine. Filtering to stop-related data is estimated to retain under 10% before the final dataset is prepared; actual size is pending measurement.
3. **Faults per machine:** The study uses a shared set of 10 stop types for both machines. Across both machines, these account for approximately 5,000-6,000 events in six months, out of approximately 11,000 events across all stop types. Exact occurrence counts for each selected stop type, separately for each machine, can be calculated after full data access. An equal split between machines must not be assumed.

These answers distinguish stop types from event occurrences. The user confirms that acceptance of an aggregated dataset in place of raw signal series is currently under discussion with the professor; no agreement has been confirmed.

## Confirmed knowledge

- The machine sensor data includes more than 300 attributes, with the same sensor attributes on both machines. Missing readings have not yet been assessed.
- Examples include valve pressures, rotor speed, laser convergence, component on/off flags, categorical machine/component configurations, and ingredients used.
- Attributes have varied units and value types: pressure, speed, position, categorical values, and binary states such as on/off and alert/normal. Exact units are not yet specified.
- This describes the overall attribute set. It does not yet distinguish static machine metadata from values recorded over time. Configuration and ingredient attributes must not be assumed static without confirmation.
- Exact attribute inventory, pseudonymized names/IDs, numerical ranges, and categorical value sets remain unconfirmed.
- There are two source machines available for the study. They have the same sensor attributes and almost the same value behavior, as described by the user.
- The user identifies machine ID as the only fixed value: it remains constant for each machine and differs between the two machines. No additional static machine variables have been identified.
- The pseudonymized study dataset will contain two machines' worth of data, corresponding to the two source machines.
- Six months of runtime data is approximately 100+ GB per machine (approximately 200+ GB across both machines).
- The study focuses on machine-stop classification. The user estimates that filtering to sensor data related to machine stops can retain just under 10% of the full data. This is an estimate, not a measured filtered size; the exact filtering rule is not yet defined.
- Machine operators maintain an Excel knowledge table describing different machine stops, possible causes, and remedies. Whether it contains timestamped event records linked to sensor data is not yet confirmed.
- The project will study the top 10 most common machine stops. This establishes an intended scope of 10 stop types/classes; it does not establish the number of individual stop occurrences per machine.
- The same top 10 stop types are shared between both machines, which are of the same kind and perform almost the same functionality. There is one shared set of 10 classes, not separate top-ten sets per machine. The number of recorded occurrences of each type per machine remains unconfirmed.
- The user estimates approximately 11,000 stop events across both machines combined, including stop types beyond the selected top 10.
- Restricting to the shared top 10 stop types gives approximately 5,000-6,000 occurrences across both machines combined. Both this estimate and the approximately 11,000 total stop events cover the same six-month study period. Counts per machine and per stop type remain unknown.
- Every stop event has an associated UTC timestamp. Labels are available for the training and test data.
- Sensor readings are recorded at sub-second, millisecond-scale intervals. The user observes that all sensors appear to record at the same interval; this has not yet been verified against the data. The exact interval and regularity remain unconfirmed, so the number of time points cannot yet be calculated.
- Full runtime sensor data is available. The proposed preprocessing selects a 10-second window around each stop-message UTC timestamp: 7 seconds before the stop and 3 seconds after it. This window is provisional and may change.
- Selected sensor data will be aggregated around stop timestamps. Candidate numerical statistics include minimum, maximum, and standard deviation; the final aggregation methods remain undecided. Treatment of categorical and binary attributes remains open.
- The deliverable will be the final dataset used for classification, with all included attributes supplied under anonymized names. Raw sensor data will not be provided.
- The derivation of the classification dataset from raw data will be explained in detail, including the eventual filtering, windowing, and aggregation decisions. These decisions are not all finalized yet.
- The professor's request for signal series needs reconciliation with this delivery scope: raw series will not be shared. Ranges and readings per stop window can be determined after full data access; their reporting format remains undecided.
- Attribute anonymization means replacing the organization's exact names with generic descriptive names, such as `roto1` or `laser_left`, while preserving an indication of the sensor's purpose. This is name replacement, not a claim that all identifying information has been removed.
- Numerical attribute minimum/maximum values and categorical/binary possible values can be determined after the thesis is agreed and the organization provides the full raw data. They are not available to report now.
- Each row of the final classification dataset will represent one stop event, with aggregated sensor features and its stop-type label. The estimated 5,000-6,000 selected stop occurrences are a provisional candidate row count before any exclusions during preprocessing; the final row count is not yet known.
- Rows from the two machines will be appended into one dataset. The user does not currently consider machine identity essential for classification, but confirms that retaining a pseudonymized machine ID is possible if needed. Its inclusion is not yet agreed.
- Recommendation: retain machine ID as metadata to support per-machine event counts and evaluation. This does not require using it as a classification feature.
- The user confirms that the exact sensor sampling interval and number of readings in each stop window can be determined once the full raw data is received. These measurements are pending data access.
- The user confirms that occurrences of each of the selected 10 stop types can also be counted separately for each machine after full data access.

## Questions to answer

1. What data will be provided for each pseudonymized machine?
   - Static machine data: pseudonymized variable names and the range for each variable.
   - For each sensor time series:
     - Pseudonymized sensor ID.
     - Sensor value range.
     - Signal series.
     - Number of time points.
2. How many pseudonymized machines will be made?
3. How many faults will there be per pseudonymized machine?

## Pending measurements and decisions

- After data access: compile the attribute inventory, units, generic names, observed numerical ranges, and categorical/binary possible values. Operating limits have not been established.
- After data access: measure exact sampling intervals and readings per stop window, assess missing readings, and report final dataset size and row count.
- After data access: count occurrences by machine and selected stop type.
- Finalize window duration and aggregation methods, including treatment of categorical and binary values.
- Decide whether to retain machine ID as metadata; this is possible and recommended but not yet agreed.
- Discuss with the professor whether the derived classification dataset and detailed methodology satisfy the request for signal series, and whether time-point counts should describe source readings, derived event rows, or both.

Exact ranges, time-series lengths, retained data size, and fault counts remain to be confirmed. Machine count is confirmed as two.
