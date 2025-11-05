# NWB Combine Capsule

This capsule combines one **primary** NWB file with one or more **secondary** NWB files into a single unified NWB session file.  
It is typically used to merge data streams from different modalities (e.g., ephys, behavior, eye tracking) into one standardized NWB dataset.

Currently, this capsule does not support the `ndx-events` extension, but future support is planned. 

---

## Input

The input directory should contain one **primary** folder and one or more **secondary** folders, named and structured as follows:
```plaintext
📦data
 ┣ 📂nwb_primary
 ┣ ┣ <session_id>.nwb
 ┣ 📂nwb_secondary_<modality>
 ┣ ┣ <session_id>.nwb
...
```
Files should follow [AIND NWB file standards](https://github.com/AllenNeuralDynamics/aind-file-standards/blob/main/docs/file_formats/nwb.md).

Additionally, the `output_format` args input is used to define the file_io format(zarr or HDF5) of the output NWB file. 
## Output

This output file contains data from all input NWB sources, with content merged into a singular NWB file.

---

## Notes

- The `nwb_primary` file serves as the base NWB — all other NWBs are merged into it in sequence.  
- Supports both `.nwb` (HDF5) and `.nwb.zarr` formats depending on configuration (`output_format` setting).  
- Empty or missing secondary folders are safely ignored with a warning.  
- Logging is provided to trace each merge step and output file path.
