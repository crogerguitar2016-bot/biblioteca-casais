[app]

title = Biblioteca de Casais
package.name = bibliotecacasais
package.domain = com.croger

source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,atlas

version = 1.0.0

requirements = python3,kivy

orientation = portrait

fullscreen = 0

android.archs = arm64-v8a

android.minapi = 23
android.api = 36

android.permissions = READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,MANAGE_EXTERNAL_STORAGE

android.accept_sdk_license = True

android.allow_backup = False

p4a.branch = develop

[buildozer]

log_level = 2

warn_on_root = 1
