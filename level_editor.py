import bpy

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

# Blenderに登録するクラスリスト
classes = (
    TOPBAR_MT_my_menu,
)

# トップバーの拡張メニュークラス
class TOPBAR_MT_my_menu(bpy.types.Menu):
    #Blenderがクラスを識別する為の固有の文字列
    bl_idname = "TOPBAR_MT_my_menu"
    #メニューのラベルとして表示される文字列
    bl_label = "MyMenu"
    #著者表示用の文字列
    bl_description = "拡張メニュー by " + bl_info["author"]

    # サブメニューの描画
    def draw(self, context):
        #トップバーの「エディターメニュー」に項目（オペレータ）を追加
        self.layout.operator("wm.url_open_preset", text="Manual", icon='HELP')

# 既存のメニューにサブメニューを追加する関数
def submenu(self, context):
    # ID指定でサブメニューを追加
    self.layout.menu(TOPBAR_MT_my_menu.bl_idname)


#Add-On有効化時コールバック
def register():
    for cls in classes:
        bpy.utils.register_class(cls)
        
    # トップバーのメニューに、作成したサブメニューを追加
    bpy.types.TOPBAR_MT_editor_menus.append(submenu)
    print("レベルエディタが有効化されました。")

#Add-On無効化時コールバック
def unregister():
    # トップバーのメニューから、サブメニューを削除
    bpy.types.TOPBAR_MT_editor_menus.remove(submenu)
    
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
        
    print("レベルエディタが無効化されました。")

if __name__ == "__main__":
    register()

