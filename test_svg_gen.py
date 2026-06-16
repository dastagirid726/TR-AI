#!/usr/bin/env python
"""Quick test of SVG generator"""
import sys
sys.path.insert(0, 'backend')

from backend.app.utils.svg_generator import (
    generate_2d_floor_plan,
    generate_3d_exterior,
    generate_3d_interior,
    generate_construction_blueprint
)

# Test 2D floor plan
print("Testing 2D Floor Plan...")
svg_2d = generate_2d_floor_plan('residential', 5000, 2)
print(f"✓ Generated 2D floor plan: {len(svg_2d)} characters")
assert '<svg' in svg_2d
assert 'Floor Plan' in svg_2d

# Test 3D exterior
print("Testing 3D Exterior...")
svg_3d_ext = generate_3d_exterior('residential', 2, 'concrete')
print(f"✓ Generated 3D exterior: {len(svg_3d_ext)} characters")
assert '<svg' in svg_3d_ext
assert 'window' in svg_3d_ext.lower()

# Test 3D interior
print("Testing 3D Interior...")
svg_3d_int = generate_3d_interior('residential', 'concrete')
print(f"✓ Generated 3D interior: {len(svg_3d_int)} characters")
assert '<svg' in svg_3d_int
assert 'sofa' in svg_3d_int.lower() or 'living' in svg_3d_int.lower()

# Test construction blueprint
print("Testing Construction Blueprint...")
svg_blueprint = generate_construction_blueprint('residential', 5000, 2)
print(f"✓ Generated blueprint: {len(svg_blueprint)} characters")
assert '<svg' in svg_blueprint
assert 'blueprint' in svg_blueprint.lower() or 'BLUEPRINT' in svg_blueprint

print("\n✅ All SVG generator tests passed!")
