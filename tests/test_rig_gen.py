import bpy
import unittest
import os
import sys
import time

project_root = os.path.dirname(os.path.dirname(__file__))
if project_root not in sys.path:
    sys.path.append(project_root)

class TestUE5RigGeneration(unittest.TestCase):

    def setUp(self):
        """Standard Setup: Clear the scene and ensure the 'tmp' directory exists."""
        bpy.ops.wm.read_factory_settings(use_empty=True)
        
        # Create tests/tmp directory if it doesn't exist
        self.test_dir = os.path.dirname(__file__)
        self.tmp_dir = os.path.join(self.test_dir, "tmp")
        if not os.path.exists(self.tmp_dir):
            os.makedirs(self.tmp_dir)

        # Ensure the addon is enabled
        addon_name = "unreal_rig_utils"
        if addon_name not in bpy.context.preferences.addons:
            bpy.ops.preferences.addon_enable(module=addon_name)

    def tearDown(self):
        """Standard Teardown: Clear the scene."""
        bpy.ops.wm.read_factory_settings(use_empty=True)

    def save_temp_file(self, filename):
        """Helper to save the current state to the tmp directory."""
        filepath = os.path.join(self.tmp_dir, f"{filename}.blend")
        bpy.ops.wm.save_as_mainfile(filepath=filepath)
        print(f"  [FILE] Saved temporary test file: {filepath}")

    def test_manny_creation(self):
        """Test: Generate Manny and save a temporary blend file."""
        print("\nRunning Manny Test...")
        
        start_time = time.time()
        result = bpy.ops.myrig.create_ue5_manny()
        duration = time.time() - start_time
        
        # Validations
        self.assertEqual(result, {'FINISHED'})
        obj = bpy.data.objects.get("UE5_Manny")
        self.assertIsNotNone(obj, "Manny object was not created")
        
        # Save temp file for manual inspection
        self.save_temp_file("test_result_manny")
        print(f"  [BENCHMARK] Manny took {duration:.4f}s")

    def test_quinn_creation(self):
        """Test: Generate Quinn and save a temporary blend file."""
        print("\nRunning Quinn Test...")
        
        start_time = time.time()
        result = bpy.ops.myrig.create_ue5_quinn()
        duration = time.time() - start_time
        
        # Validations
        self.assertEqual(result, {'FINISHED'})
        obj = bpy.data.objects.get("UE5_Quinn")
        self.assertIsNotNone(obj, "Quinn object was not created")
        
        # Save temp file for manual inspection
        self.save_temp_file("test_result_quinn")
        print(f"  [BENCHMARK] Quinn took {duration:.4f}s")

    def test_bone_collections_v5(self):
        """Verify Blender 5.0 Bone Collections on Manny."""
        bpy.ops.myrig.create_ue5_manny()
        arm_data = bpy.data.objects["UE5_Manny"].data
        self.assertIn("Deform", arm_data.collections.keys(), "Deform collection missing")

def run_tests():
    suite = unittest.TestLoader().loadTestsFromTestCase(TestUE5RigGeneration)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    if not result.wasSuccessful():
        sys.exit(1)

if __name__ == "__main__":
    run_tests()