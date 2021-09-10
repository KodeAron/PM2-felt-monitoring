# PM2feltUFF

Program for managing data from paper machine PM2 to look for indications on felt degradation.

## aspen.py
Read process data from xlsx files created with Aspen. Not implemented.

## extractombiner.py
Extract and combine data from the dataframe-pickle-file created by observer_merge.py

## feature_importance.py
Feature importance test on feature dataframe.

## feltdata.py
Read xlsx file holding data on felt replacement dates.

## generaltools.py
Supporting functions that are used in several of the other modules.

## observer_merge.py
Utilise observer_uff.py and observer_xml.py to create one dataframe containing all raw data. Dataframe saved as pickle file.

## observer_uff.py
Load observer data from UFF files.

## observer_xml.py
Load observer data from XML files.

## plot_ffts.py
Plot ffts from the raw vibration data in the dataframe-pickle-file.

## plot_merged_data.py
Create plots containing information from several sources; Observer, ProTAK, felt data.

## plot_raw.py
Plot raw vibration data in the dataframe-pickle-file.

## protak.py
Read availability data from xlsx files exported from ProTAK.
