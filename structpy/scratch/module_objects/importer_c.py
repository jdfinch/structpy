
import structpy.scratch.module_objects.importer_a as importer_a
import structpy.scratch.module_objects.importer_b as importer_b

print(importer_a)
print(importer_b)
print(importer_a.module)
print(importer_b.module)
print(importer_a.module is importer_b.module)