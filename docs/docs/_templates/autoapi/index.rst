StarSteer Python Calculator Documentation
=========================================

StarSteer Python Calculator is a comprehensive tool for managing StarSteer objects using Python. This documentation provides detailed information about the available StarSteer objects API with examples of their usage.

SS Objects API
--------------

.. toctree::
   :titlesonly:

   /autoapi/rogii_solo/base/index
   /autoapi/rogii_solo/client/index
   /autoapi/rogii_solo/earth_model/index
   /autoapi/rogii_solo/horizon/index
   /autoapi/rogii_solo/interpretation/index
   /autoapi/rogii_solo/log/index
   /autoapi/rogii_solo/mudlog/index
   /autoapi/rogii_solo/project/index
   /autoapi/rogii_solo/target_line/index
   /autoapi/rogii_solo/topset/index
   /autoapi/rogii_solo/trajectory/index
   /autoapi/rogii_solo/types/index
   /autoapi/rogii_solo/well/index


Code Styling
------------

All Python scripts are written following the PEP 8 guidelines and formatted using tools like Ruff. Additionally, scripts adhere to a consistent style for importing libraries, calling variables, classes, and methods. Here is an example of simple script with correct code style to start with:

**Example : Create a Top centered between Starred Top and Starred Bottom ones**

.. code-block:: python

   import sys

   from pathlib import Path

   version = ''.join(map(str, sys.version_info[:2]))
   addPath(f'{Path.home()}/AppData/Local/StarSteer/PythonLibraries{version}')

   import numpy 

   INPUT_WELL = InputWell
   TOPSET = InputTopset
   WELLS = Wells


   def set_center_top(topset, upper_top, bottom_top):
      mean_md = np.mean([upper_top.MD, bottom_top.MD])
      top_name = 'Center Top'
      topset.addRow(top_name, mean_md)
      topset.Tops[top_name].setStarred(TargetFlags.Center)


   def main():
      topset = WELLS[INPUT_WELL].TopSets[TOPSET]
      upper_top = topset.Tops[TargetFlags.Top]
      bottom_top = topset.Tops[TargetFlags.Bottom]
      set_center_top(topset=topset, upper_top=upper_top, bottom_top=bottom_top)
      center_top = topset.Tops[TargetFlags.Center]
      print(f'New Top has md = {center_top.MD} and name "{center_top.name}".')


   if __name__ == '__main__':
      try:
         main()
      except Exception as exception:
         print(exception)


To explore more examples, refer to the KB Python Script Database (https://kb.solo.cloud/Python+Script+Database) or Templates scripts in the StarSteer Calculator.
