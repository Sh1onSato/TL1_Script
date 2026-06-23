import bpy
import math
import bpy_extras

# ブレンダーに登録するアドオン情報
bl_info = {
    "name": "レベルエディタ",
    "author": "Sato Shion",
    "version": (1, 0),
    "blender": (3, 3, 1),
    "location": "",
    "description": "レベルエディタ",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Object"
}

# オペレータ：頂点を伸ばす
class MYADDON_OT_stretch_vertex(bpy.types.Operator):
    bl_idname = "myaddon.myaddon_ot_stretch_vertex"
    bl_label = "頂点を伸ばす"
    bl_description = "頂点座標を引っ張って伸ばします"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.data.objects["Cube"].data.vertices[0].co.x += 1.0
        print("頂点を伸ばしました。")
        return {'FINISHED'}


# オペレータ：ICO球生成
class MYADDON_OT_create_ico_sphere(bpy.types.Operator):
    bl_idname = "myaddon.myaddon_ot_create_object"
    bl_label = "ICO球生成"
    bl_description = "ICO球を生成します"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.mesh.primitive_ico_sphere_add()
        print("ICO球を生成しました。")
        return {'FINISHED'}


# オペレータ：シーン出力（★再帰ツリー・インデント対応の完全エクスポート版！）
class MYADDON_OT_export_scene(bpy.types.Operator, bpy_extras.io_utils.ExportHelper):
    bl_idname = "myaddon.myaddon_ot_export_scene"
    bl_label = "シーン出力"
    bl_description = "シーン情報をExportします"

    # 出力するファイルの拡張子を指定
    filename_ext = ".scene"

    def write_and_print(self, file, str):
        print(str)          # コンソールに出力
        file.write(str)     # ファイルに文字列を書き込む
        file.write('\n')    # 自動で改行文字を書き込む


    def parse_scene_recursive(self, file, object, level):
        
        # 階層の深さ（level）の数だけ、文字列としてのタブ文字（\t）を作成
        indent = ''
        for i in range(level):
            indent += "\t"
            
        # オブジェクト種別と名前の書き込み（先頭にインデントを合体）
        self.write_and_print(file, indent + object.type + " - " + object.name)
        
        # ローカルトランスフォーム行列から平行移動、回転、スケーリングを抽出
        trans, rot, scale = object.matrix_local.decompose()
        
        # 回転を Quaternion から Euler に変換
        rot = rot.to_euler()
        
        # ラジアンから度数法に変換
        rot.x = math.degrees(rot.x)
        rot.y = math.degrees(rot.y)
        rot.z = math.degrees(rot.z)
        
        # トランスフォーム情報をファイルとコンソールに出力（先頭にインデントを合体）
        self.write_and_print(file, indent + "Trans(%f,%f,%f)" % (trans.x, trans.y, trans.z) )
        self.write_and_print(file, indent + "Rot(%f,%f,%f)" % (rot.x, rot.y, rot.z) )
        self.write_and_print(file, indent + "Scale(%f,%f,%f)" % (scale.x, scale.y, scale.z) )
        self.write_and_print(file, '') # オブジェクト間の区切り空行

        for child in object.children:
            self.parse_scene_recursive(file, child, level + 1)


    def export(self):
        """ファイルに出力"""
        print("シーン情報出力開始... %r" % self.filepath)

        # ファイルをテキスト形式で書き出し用にオープン
        with open(self.filepath, "wt") as file:
            self.write_and_print(file, "SCENE")
            self.write_and_print(file, "")
            for object in bpy.context.scene.objects:
                if not object.parent:
                    self.parse_scene_recursive(file, object, 0)
            
        print("シーン情報出力完了！")


    def execute(self, context):
        print("シーン情報をExportします")

        # ファイル書き出し関数を実行
        self.export()

        print("シーン情報をExportしました")
        self.report({'INFO'}, "シーン情報をExportしました")

        return {'FINISHED'}


# トップバーの拡張メニュークラス
class TOPBAR_MT_my_menu(bpy.types.Menu):
    bl_idname = "MYADDON_MT_my_menu"
    bl_label = "MyMenu"
    bl_description = "拡張メニュー by " + bl_info["author"]

    def draw(self, context):
        self.layout.operator(MYADDON_OT_stretch_vertex.bl_idname,
                             text=MYADDON_OT_stretch_vertex.bl_label)
        self.layout.operator(MYADDON_OT_create_ico_sphere.bl_idname,
                             text=MYADDON_OT_create_ico_sphere.bl_label)
        self.layout.operator(MYADDON_OT_export_scene.bl_idname,
                             text=MYADDON_OT_export_scene.bl_label)


# 既存のメニューにサブメニューを追加する関数
def submenu(self, context):
    self.layout.menu(TOPBAR_MT_my_menu.bl_idname)

classes = (
    TOPBAR_MT_my_menu,
    MYADDON_OT_stretch_vertex,
    MYADDON_OT_create_ico_sphere,
    MYADDON_OT_export_scene,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.TOPBAR_MT_editor_menus.append(submenu)
    print("レベルエディタが有効化されました。")

def unregister():
    bpy.types.TOPBAR_MT_editor_menus.remove(submenu)
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    print("レベルエディタが無効化されました。")
    
if __name__ == "__main__":
    register()

