# Kaprao asset validation

The final GLB passes the reproducible checks in `Tools/kaprao_validate.py`.

| Property | Measured result |
| --- | --- |
| Runtime triangles | 19,900: body 18,000; removable shades 1,900 |
| Mesh nodes | 2 |
| Skin / joints | 1 shared skin / 10 joints |
| Materials / primitives | 15 materials / 16 material primitives |
| Clips | `Idle_Look`, `Walk_InPlace`, `Jump_Fall`, `Celebrate` |
| Root motion | Zero translation in all four exported clips |
| Loop endpoints | Idle and walk repeat to floating-point tolerance |
| Mesh data | Finite positions/normals/weights, in-range indices and joints |
| Normals / weights | Unit normals and normalized weights within stated tolerances |
| Degenerate triangles | Zero |
| Floor | Y = 0 within 0.005 m tolerance |
| Collision / studio | Excluded from every runtime exchange file |
| Axis convention | Meters; Y up; character faces +X |

The source has genuine smooth geometry, a material-based white forehead blaze, sculpted cream face and chest, separate dark RGB sunglasses, and a teal scarf. Hero, plain-face, orthographic, and motion previews are rendered from the delivered Blender mesh. There is no image-generation substitution for these model previews. No depth of field or motion blur is enabled.

The rig uses rigid weighted mesh islands. This is an intentional first-demo animation approach, not a production organic quadruped deformation rig. Jump/fall is a pose sequence; gameplay owns the world trajectory. The two looped clips have no root translation. Shadows and floor in the previews belong only to the source studio collection.

Separate animated USD files retain the four action ranges for native import testing. The coordinator owns native SceneKit, conversion/reload, and simulator acceptance evidence. This report establishes file integrity and Blender rendering, and does not assert that Duo gameplay integration has passed.
