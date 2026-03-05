# -*- mode: python ; coding: utf-8 -*-
# PyInstaller spec file for PDF Flipbook Animator Windows executable

import os
import sys
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

block_cipher = None

# Collect all template files
template_datas = collect_data_files('pdf_flipbook_animator', subdir='templates')

a = Analysis(
    ['src/pdf_flipbook_animator/__main__.py'],
    pathex=[],
    binaries=[],
    datas=template_datas,
    hiddenimports=[
        'pdf_flipbook_animator',
        'pdf_flipbook_animator.cli',
        'pdf_flipbook_animator.config',
        'pdf_flipbook_animator.core',
        'pdf_flipbook_animator.core.converter',
        'pdf_flipbook_animator.core.generator',
        'pdf_flipbook_animator.utils',
        'pdf_flipbook_animator.utils.image',
        'click',
        'PIL',
        'PIL._imaging',
        'fitz',
        'pymupdf',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'matplotlib',
        'numpy',
        'pandas',
        'scipy',
        'tkinter',
        'test',
        'unittest',
        'pydoc',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='pdf-flipbook',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='pdf-flipbook',
)
