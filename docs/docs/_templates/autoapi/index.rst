SDK Python Documentation
=========================================

Python SDK is a comprehensive tool for managing ROGII SOLO objects using Python by directing to the Python SDK API.
This documentation provides detailed information about the available SDK objects API with examples of their usage.

Python SDK Objects API
--------------

.. toctree::
   :titlesonly:

   Project </autoapi/rogii_solo/project/index>
   Well </autoapi/rogii_solo/well/index>
   Trajectory </autoapi/rogii_solo/trajectory/index>
   Interpretation </autoapi/rogii_solo/interpretation/index>
   Horizon </autoapi/rogii_solo/horizon/index>
   Mudlog </autoapi/rogii_solo/mudlog/index>
   Topset </autoapi/rogii_solo/topset/index>
   Target Line </autoapi/rogii_solo/target_line/index>
   Log </autoapi/rogii_solo/log/index>
   Trace </autoapi/rogii_solo/trace/index>
   Comment </autoapi/rogii_solo/comment/index>
   Earth Model </autoapi/rogii_solo/earth_model/index>
   Base </autoapi/rogii_solo/base/index>
   Client </autoapi/rogii_solo/client/index>
   PAPI Client </autoapi/rogii_solo/papi/client/index>


Code Styling
------------

All Python SDK scripts are written following the PEP 8 guidelines and formatted using tools like Ruff. Additionally, 
scripts adhere to a consistent style for importing libraries, calling variables, classes, and methods. 


**Example : Create a Well**

.. code-block:: python

   from rogii_solo import SoloClient

   CLIENT_ID = ... # Input your client ID
   CLIENT_SECRET = ... # Input your client secret
   PROJECT_NAME = 'Project1'
   WELL_NAME = 'Well1'
   API = '001-123-1236'
   OPERATOR = 'Schl'
   CONVERGENCE = 0.1
   AZIMUTH = 12
   KB = 132
   TIE_IN_TVD = 2456
   TIE_IN_NS = 145
   TIE_IN_EW = 1643
   XS_RF_REAL = 643826
   YS_RF_REAL = 83461678


   def create_well(solo_client: SoloClient):
      project = solo_client.set_project_by_name(PROJECT_NAME)

      project.create_well(
         name=WELL_NAME,
         api=API,
         operator=OPERATOR,
         convergence=CONVERGENCE,
         azimuth=AZIMUTH,
         kb=KB,
         tie_in_tvd=TIE_IN_TVD,
         tie_in_ns=TIE_IN_NS,
         tie_in_ew=TIE_IN_EW,
         xsrf_real=XS_RF_REAL,
         ysrf_real=YS_RF_REAL,
      )


   def main():
      solo_client = SoloClient(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
      create_well(solo_client)
      print(project.wells.find_by_name('Well1').to_dict())


   if __name__ == '__main__':
      try:
         main()
      except Exception as exception:
         print(exception)
