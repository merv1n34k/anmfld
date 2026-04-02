"""
Convert generator_cropped.dxf to STEP via cadquery's importDXF.

Removes stray entity 62 (dangling line) before import,
then exports 2D face and 3D extruded solid.
"""

import ezdxf
import cadquery as cq

DXF_PATH = "generator.dxf"
CLEAN_DXF_PATH = "generator_clean.dxf"
STEP_2D_PATH = "generator_2d.step"
STEP_3D_PATH = "generator_3d.step"

# DXF units → mm: main channel = 3.175 DXF units = 0.125 mm
SCALE = 0.125 / 3.175  # ~0.03937
DEPTH_MM = 0.125  # 125 um channel depth


def clean_dxf():
    """Remove stray entity 62 (dangling line not part of channel walls)."""
    doc = ezdxf.readfile(DXF_PATH)
    msp = doc.modelspace()
    entities = list(msp)
    print(f"Original: {len(entities)} entities")
    msp.delete_entity(entities[62])
    doc.saveas(CLEAN_DXF_PATH)
    print(f"Cleaned: {len(entities) - 1} entities → {CLEAN_DXF_PATH}")


def main():
    print("=" * 60)
    print("DXF → STEP Converter")
    print("=" * 60)

    # Step 1: Remove stray line
    clean_dxf()

    # Step 2: Import clean DXF
    print("\nImporting clean DXF...")
    result = cq.importers.importDXF(CLEAN_DXF_PATH, tol=0.001)
    faces = result.faces().vals()
    wires = result.wires().vals()
    print(f"  {len(wires)} wire(s), {len(faces)} face(s)")

    if not faces:
        print("FATAL: No faces created. Check DXF geometry.")
        return

    bb = result.val().BoundingBox()
    print(f"  BB (DXF units): X=[{bb.xmin:.4f}, {bb.xmax:.4f}] Y=[{bb.ymin:.4f}, {bb.ymax:.4f}]")
    print(f"  Size: {bb.xmax - bb.xmin:.4f} x {bb.ymax - bb.ymin:.4f}")

    # Step 3: Scale to mm
    print(f"\nScaling by {SCALE:.5f} (DXF units → mm)...")
    scaled = result.val().scale(SCALE)
    result_mm = cq.Workplane("XY").newObject([scaled])
    bb2 = scaled.BoundingBox()
    print(f"  BB (mm): X=[{bb2.xmin:.4f}, {bb2.xmax:.4f}] Y=[{bb2.ymin:.4f}, {bb2.ymax:.4f}]")
    print(f"  Size: {bb2.xmax - bb2.xmin:.4f} x {bb2.ymax - bb2.ymin:.4f} mm")

    # Step 4: Export 2D face (mm)
    cq.exporters.export(result_mm, STEP_2D_PATH)
    print(f"\n✓ 2D face STEP: {STEP_2D_PATH}")

    # Step 5: Extrude to 3D (depth = 0.125 mm)
    try:
        solid = result_mm.extrude(DEPTH_MM)
        cq.exporters.export(solid, STEP_3D_PATH)
        print(f"✓ 3D solid STEP: {STEP_3D_PATH} (extruded {DEPTH_MM} mm = {DEPTH_MM * 1000:.0f} um)")
    except Exception as e:
        print(f"  3D extrusion failed: {e}")
        print("  (Use 2D STEP and extrude in SpaceClaim instead)")

    print("Done. All dimensions in mm.")


if __name__ == "__main__":
    main()
