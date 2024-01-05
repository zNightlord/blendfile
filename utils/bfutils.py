from . import blendfile
from ..blendfile import BlendFile, BlendFileBlock
  
import typing
import numpy as np
from pprint import pprint
  
FieldPath = typing.Union[bytes, typing.Iterable[typing.Union[bytes, int]]]
AR_BONE_FIRST = (b'bonebase', b'first')
AR_CHILD_FIRST = (b'childbase', b'first')
  
def listbase(
    block: typing.Optional[BlendFileBlock], next_path: FieldPath = b"next"
) -> typing.Iterator[BlendFileBlock]:
  """Generator, yFieldPath = typing.Union[bytes, typing.Iterable[typing.Union[bytes, int]]]
  yields all blocks in the ListBase linked list.
  """
  while block:
      yield block
      next_ptr = block[next_path]
      if next_ptr == 0:
          break
      block = block.file.block_from_offset[next_ptr]

def get_ID_name(ID):
  return ID[b'id', b'name'][2:].decode('utf-8')

def get_ID_type(ID):
  return [b'id', b'name'][:2].decode('utf-8')

def get_collection_objects(collection):
  all_objects = set()
  collection_objects = collection.get_pointer((b'gobject', b'first'))
  # if ListBase is empty then it returns `None`
  if collection_objects is not None:
    for collection_obj in listbase(collection_objects):
        obj = collection_obj.get_pointer(b"ob")
        all_objects.add(obj)
  collection_children = collection.get_pointer((b'children', b'first'))
  if collection_children is not None:
    for collection_child in listbase(collection_children):
        collection = collection_child.get_pointer(b"collection")
        all_objects.update(get_collection_objects(collection))
  return all_objects
  
def get_armature_bones(armature_data, use_list=True, debug=False):
  if get_ID_type(armature_data) != "AR":
    return
  bone_set = set()
  bone_list = list()
  roots = armature.get_pointer(AR_BONE_FIRST)
  if roots is not None:
    # print(roots[b'name'])
    for b in listbase(roots):
      if debug:
        print(b[b'name'])
      bone_list.append(b)
      bone_set.add(b)
      get_bone_children(b, bone_set, bone_list, debug=debug)
  return bone_list if use_list else bone_set
      
def get_bone_children(bone, bone_set, bone_list, i=0, debug=False):
  bones = bone.get_pointer(AR_CHILD_FIRST)
  
  if bones is not None:
    i +=1
    for b in listbase(bones):
      bone_set.add(b)
      if debug:
        if not b in bone_list:
          print("|"+"-"*i, b[b'name'])
      bone_list.append(b)
      get_bone_children(b, bone_set, bone_list, i)
        
def get_mesh_verts(obj_data):
  # TODO better mask, delete index
  verts = obj_data.get_pointer(b'mvert')
  v_data  = verts.get_raw_data(b'float')
  va = np.asarray(v_data)
  return va[va!=v_data[3]].reshape(-1,3))

def get_mesh_edges(obj_data):
  edges = obj_data.get_pointer(b'medge')
  e_data = edges.get_raw_data(b'int')
  ea = np.asarray(e_data)
  return ea[ea!=e_data[2]].reshape(-1,2)

def get_mesh_faces(obj_data, is_tris=False):
  faces = obj_data.get_pointer(b'mface')
  e_data = edges.get_raw_data(b'int')
  ea = np.asarray(e_data)
  face_vert = 3 if is_tris else 4
  return ea[ea!=e_data[face_vert]].reshape(-1, face_vert)

def load_blend_scenes(filepath, scene_name=None):
  with blendfile.open_blend(filepath) as blend:
    scenes = [b for b in blend.blocks if b.code == b'SC']
    if scene_name is None:
      return scenes
    else:
      for scene in scenes:
        name = get_ID_name(scene)
        if name == scene_name:
          return scene
    # path = scene[b'r', b'pic'].decode('utf-8')
    # frame_start = scene[b'r', b'sfra']
    # frame_end = scene[b'r', b'efra']

def get_scene_collections(scene):
  collections = set()
  scene_col = scene.get_pointer(b'master_collection')
  child_col = scene_col.get_pointer((b'children', b'first'))
  if child_col is not None:
    for c in listbase(child_col):
      c = collection_child.get_pointer(b"collection")
      collections.add(c)
  return collections

def get_mesh_data(obj_data):
  if get_ID_type(obj_data) = 'ME':
    verts = get_mesh_verts(obj_data)
    edges = get_mesh_edges(obj_data)
    faces = get_mesh_faces(obj_data)
  return verts, edges, faces
