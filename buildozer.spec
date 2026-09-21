[app]

title = Biblioteca de Casais
package.name = bibliotecacasais
package.domain = com.croger

source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,atlas,pdf,htm,html,doc,docx,ppt,pptx,txt,epub

android.add_resources = android_res/xml
android.add_src = android_src

android.gradle_dependencies = androidx.core:core:1.13.1
android.enable_androidx = True
android.extra_manifest_application_arguments = ./android_provider.xml

version = 1.0.0

requirements = python3,kivy,pyjnius,android

orientation = portrait

fullscreen = 0

android.archs = arm64-v8a

android.minapi = 24
android.api = 36

android.permissions = READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,MANAGE_EXTERNAL_STORAGE

android.accept_sdk_license = True

android.allow_backup = False

p4a.branch = develop

[buildozer]

log_level = 2
warn_on_root = 1
