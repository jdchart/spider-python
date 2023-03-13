''' ================================================================================
TEST SCRIPT
Check everything is working.
================================================================================ '''
import os
import shutil
print("\nRunning tests...")

# Module import:
print("\nImporting spider...")
import spider as sp
print("\tSpider imported succesfully.")

# Web creation and load
print("\nCreating a web...")
testWeb = sp.createWeb({"path" : os.path.join(os.getcwd(), "test_web")})
print("\tCreated web succesfully.")

print("Loading a web...")
loadedWeb = sp.loadWeb(testWeb.path)
print("\tLoaded web succesfully.")





# Cleanup
print("\nCleaning up...")
if os.path.exists(testWeb.path):
    shutil.rmtree(testWeb.path)
print("Finished!\n")