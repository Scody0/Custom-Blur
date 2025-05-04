import tkinter as tk
from tkinter import ttk, messagebox
import pygetwindow as gw
import ctypes
import customtkinter as ctk
from collections import deque
import json
import os
import logging
from datetime import datetime

GWL_EXSTYLE = -20
WS_EX_LAYERED = 0x80000
LWA_ALPHA = 0x2
ACCENT_ENABLE_BLURBEHIND = 3
ACCENT_ENABLE_ACRYLICBLURBEHIND = 4
WCA_ACCENT_POLICY = 19
DWMWA_EXTENDED_FRAME_BOUNDS = 9

user32 = ctypes.windll.user32
dwmapi = ctypes.windll.dwmapi
SetWindowLong = user32.SetWindowLongW
GetWindowLong = user32.GetWindowLongW
SetLayeredWindowAttributes = user32.SetLayeredWindowAttributes
SetWindowCompositionAttribute = user32.SetWindowCompositionAttribute
DwmSetWindowAttribute = dwmapi.DwmSetWindowAttribute

class ACCENT_POLICY(ctypes.Structure):
    _fields_ = [
        ("AccentState", ctypes.c_int),
        ("AccentFlags", ctypes.c_int),
        ("GradientColor", ctypes.c_int),
        ("AnimationId", ctypes.c_int)
    ]

class WINDOWCOMPOSITIONATTRIBDATA(ctypes.Structure):
    _fields_ = [
        ("Attribute", ctypes.c_int),
        ("Data", ctypes.c_void_p),
        ("SizeOfData", ctypes.c_size_t)
    ]

LOCALIZATION = {
    "en": {
        "title": "Custom Blur",
        "windows": "Windows",
        "refresh": "🔄 Refresh",
        "auto_refresh": "Auto-Refresh",
        "transparency": "Transparency",
        "blur_effect": "Blur Effect",
        "enable_blur": "Enable Blur",
        "blur_type": ["Standard Blur", "Acrylic Blur"],
        "blur_opacity": "Blur Opacity",
        "blur_intensity": "Blur Intensity",
        "tint_opacity": "Tint Opacity",
        "undo": "⟲ Undo",
        "reset": "🔄 Reset",
        "about": "About",
        "save_profile": "Save Profile",
        "load_profile": "Load Profile",
        "ready": "Ready",
        "window_list_refreshed": "Window list refreshed",
        "selected": "Selected: {}",
        "window_not_found": "Window not found!",
        "transparency_set": "Transparency: {}",
        "blur_enabled": "Blur enabled",
        "blur_disabled": "Blur disabled",
        "blur_type_set": "Blur type: {}",
        "blur_opacity_set": "Blur opacity: {}",
        "blur_intensity_set": "Blur intensity: {}",
        "tint_opacity_set": "Tint opacity: {}",
        "changes_undone": "Changes undone",
        "nothing_to_undo": "Nothing to undo",
        "reset_complete": "Window reset to original state",
        "profile_saved": "Profile saved",
        "profile_loaded": "Profile loaded",
        "profile_error": "Error handling profile",
        "language": "Language",
        "error": "Error",
        "window_incompatible": "This window does not support blur effects",
        "tooltip_refresh": "Refresh the list of active windows",
        "tooltip_auto_refresh": "Automatically refresh the window list",
        "tooltip_transparency": "Adjust window transparency (50-255)",
        "tooltip_enable_blur": "Enable or disable blur effect",
        "tooltip_blur_type": "Choose between standard or acrylic blur",
        "tooltip_blur_opacity": "Adjust blur opacity (0-255)",
        "tooltip_blur_intensity": "Adjust blur strength (0-100)",
        "tooltip_tint_opacity": "Adjust background tint opacity (0-255)",
        "tooltip_undo": "Undo the last change",
        "tooltip_reset": "Reset window to original state",
        "tooltip_save_profile": "Save current settings as a profile",
        "tooltip_load_profile": "Load a saved profile",
        "tooltip_language": "Select application language",
        "tooltip_about": "View information about the program"
    },
    "ru": {
        "title": "Настраиваемый блюр",
        "windows": "Окна",
        "refresh": "🔄 Обновить",
        "auto_refresh": "Автообновление",
        "transparency": "Прозрачность",
        "blur_effect": "Эффект блюра",
        "enable_blur": "Включить блюр",
        "blur_type": ["Стандартный блюр", "Акриловый блюр"],
        "blur_opacity": "Непрозрачность блюра",
        "blur_intensity": "Интенсивность блюра",
        "tint_opacity": "Непрозрачность оттенка",
        "undo": "⟲ Отменить",
        "reset": "🔄 Сбросить",
        "about": "О программе",
        "save_profile": "Сохранить профиль",
        "load_profile": "Загрузить профиль",
        "ready": "Готово",
        "window_list_refreshed": "Список окон обновлён",
        "selected": "Выбрано: {}",
        "window_not_found": "Окно не найдено!",
        "transparency_set": "Прозрач kapalı: {}",
        "blur_enabled": "Блюр включён",
        "blur_disabled": "Блюр выключен",
        "blur_type_set": "Тип блюра: {}",
        "blur_opacity_set": "Непрозрачность блюра: {}",
        "blur_intensity_set": "Интенсивность блюра: {}",
        "tint_opacity_set": "Непрозрачность оттенка: {}",
        "changes_undone": "Изменения отменены",
        "nothing_to_undo": "Нечего отменять",
        "reset_complete": "Окно сброшено до исходного состояния",
        "profile_saved": "Профиль сохранен",
        "profile_loaded": "Профиль загружен",
        "profile_error": "Ошибка обработки профиля",
        "language": "Язык",
        "error": "Ошибка",
        "window_incompatible": "Это окно не поддерживает эффекты блюра",
        "tooltip_refresh": "Обновить список активных окон",
        "tooltip_auto_refresh": "Автоматически обновлять список окон",
        "tooltip_transparency": "Настроить прозрачность окна (50-255)",
        "tooltip_enable_blur": "Включить или отключить эффект блюра",
        "tooltip_blur_type": "Выбрать между стандартным или акриловым блюром",
        "tooltip_blur_opacity": "Настроить непрозрачность блюра (0-255)",
        "tooltip_blur_intensity": "Настроить интенсивность блюра (0-100)",
        "tooltip_tint_opacity": "Настроить непрозрачность оттенка фона (0-255)",
        "tooltip_undo": "Отменить последнее изменение",
        "tooltip_reset": "Сбросить окно в исходное состояние",
        "tooltip_save_profile": "Сохранить текущие настройки как профиль",
        "tooltip_load_profile": "Скачать сохраненный профиль",
        "tooltip_language": "Выбрать язык приложения",
        "tooltip_about": "Просмотреть информацию о приложении"
    },
    "uk": {
        "title": "Налаштований блюр",
        "windows": "Вікна",
        "refresh": "🔄 Оновити",
        "auto_refresh": "Автооновлення",
        "transparency": "Прозорість",
        "blur_effect": "Ефект блюру",
        "enable_blur": "Увімкнути блюр",
        "blur_type": ["Стандартний блюр", "Акриловий блюр"],
        "blur_opacity": "Непрозорість блюру",
        "blur_intensity": "Інтенсивність блюру",
        "tint_opacity": "Непрозорість відтінку",
        "undo": "⟲ Скасувати",
        "reset": "🔄 Скинути",
        "about": "Про програму",
        "save_profile": "Зберегти профіль",
        "load_profile": "Завантажити профіль",
        "ready": "Готово",
        "window_list_refreshed": "Список вікон оновлено",
        "selected": "Вибрано: {}",
        "window_not_found": "Вікно не знайдено!",
        "transparency_set": "Прозорість: {}",
        "blur_enabled": "Блюр увімкнено",
        "blur_disabled": "Блюр вимкнено",
        "blur_type_set": "Тип блюру: {}",
        "blur_opacity_set": "Непрозорість блюру: {}",
        "blur_intensity_set": "Інтенсивність блюру: {}",
        "tint_opacity_set": "Непрозорість відтінку: {}",
        "changes_undone": "Зміни скасовано",
        "nothing_to_undo": "Немає що скасовувати",
        "reset_complete": "Вікно скинуто до початкового стану",
        "profile_saved": "Профіль збережено",
        "profile_loaded": "Профіль завантажено",
        "profile_error": "Помилка обробки профілю",
        "language": "Мова",
        "error": "Помилка",
        "window_incompatible": "Це вікно не підтримує ефекти блюру",
        "tooltip_refresh": "Оновити список активних вікон",
        "tooltip_auto_refresh": "Автоматично оновлювати список вікон",
        "tooltip_transparency": "Налаштувати прозорість вікна (50-255)",
        "tooltip_enable_blur": "Увімкнути або вимкнути ефект блюру",
        "tooltip_blur_type": "Вибрати між стандартним або акриловим блюром",
        "tooltip_blur_opacity": "Налаштувати непрозорість блюру (0-255)",
        "tooltip_blur_intensity": "Налаштувати інтенсивність блюру (0-100)",
        "tooltip_tint_opacity": "Налаштувати непрозорість відтінку фону (0-255)",
        "tooltip_undo": "Скасувати останню зміну",
        "tooltip_reset": "Скинути вікно до початкового стану",
        "tooltip_save_profile": "Зберегти поточні налаштування як профіль",
        "tooltip_load_profile": "Завантажити збережений профіль",
        "tooltip_language": "Вибрати мову програми",
        "tooltip_about": "Переглянути інформацію про програму"
    },
    "be": {
        "title": "Наладжвальны блюр",
        "windows": "Вокны",
        "refresh": "🔄 Абнавіць",
        "auto_refresh": "Аўтаабнаўленне",
        "transparency": "Празрыстасць",
        "blur_effect": "Эфект блюру",
        "enable_blur": "Уключыць блюр",
        "blur_type": ["Стандартны блюр", "Акрылавы блюр"],
        "blur_opacity": "Непразрыстасць блюру",
        "blur_intensity": "Інтэнсіўнасць блюру",
        "tint_opacity": "Непразрыстасць адцення",
        "undo": "⟲ Адмяніць",
        "reset": "🔄 Скінуць",
        "about": "Пра праграму",
        "save_profile": "Захаваць профіль",
        "load_profile": "Загрузіць профіль",
        "ready": "Гатова",
        "window_list_refreshed": "Спіс вокнаў абноўлены",
        "selected": "Абрана: {}",
        "window_not_found": "Вокна не знойдзена!",
        "transparency_set": "Празрыстасць: {}",
        "blur_enabled": "Блюр уключаны",
        "blur_disabled": "Блюр выключаны",
        "blur_type_set": "Тып блюру: {}",
        "blur_opacity_set": "Непразрыстасць блюру: {}",
        "blur_intensity_set": "Інтэнсіўнасць блюру: {}",
        "tint_opacity_set": "Непразрыстасць адцення: {}",
        "changes_undone": "Змены адменены",
        "nothing_to_undo": "Няма чаго адмяняць",
        "reset_complete": "Вокна скінута да пачатковага стану",
        "profile_saved": "Профіль захаваны",
        "profile_loaded": "Профіль загружаны",
        "profile_error": "Памылка апрацоўкі профілю",
        "language": "Мова",
        "error": "Памылка",
        "window_incompatible": "Гэта вокна не падтрымлівае эфекты блюру",
        "tooltip_refresh": "Абнавіць спіс актыўных вокнаў",
        "tooltip_auto_refresh": "Аўтаматычна абнаўляць спіс вокнаў",
        "tooltip_transparency": "Наладзіць празрыстасць вокнаў (50-255)",
        "tooltip_enable_blur": "Уключыць або выключыць эфект блюру",
        "tooltip_blur_type": "Выбраць паміж стандартным і акрылавым блюрам",
        "tooltip_blur_opacity": "Наладзіць непразрыстасць блюру (0-255)",
        "tooltip_blur_intensity": "Наладзіць інтэнсіўнасць блюру (0-100)",
        "tooltip_tint_opacity": "Наладзіць непразрыстасць адцення фону (0-255)",
        "tooltip_undo": "Адмяніць апошнюю змену",
        "tooltip_reset": "Скінуць вокна да пачатковага стану",
        "tooltip_save_profile": "Захаваць бягучыя налады як профіль",
        "tooltip_load_profile": "Загрузіць захаваны профіль",
        "tooltip_language": "Выбраць мову прыкладання",
        "tooltip_about": "Праглядзець інфармацыю пра праграму"
    },
    "de": {
        "title": "Benutzerdefinierte Unschärfe",
        "windows": "Fenster",
        "refresh": "🔄 Aktualisieren",
        "auto_refresh": "Automatische Aktualisierung",
        "transparency": "Transparenz",
        "blur_effect": "Unschärfeeffekt",
        "enable_blur": "Unschärfe aktivieren",
        "blur_type": ["Standardunschärfe", "Acrylunschärfe"],
        "blur_opacity": "Unschärfeopazität",
        "blur_intensity": "Unschärfeintensität",
        "tint_opacity": "Tönungsopazität",
        "undo": "⟲ Rückgängig",
        "reset": "🔄 Zurücksetzen",
        "about": "Über",
        "save_profile": "Profil speichern",
        "load_profile": "Profil laden",
        "ready": "Bereit",
        "window_list_refreshed": "Fensterliste aktualisiert",
        "selected": "Ausgewählt: {}",
        "window_not_found": "Fenster nicht gefunden!",
        "transparency_set": "Transparenz: {}",
        "blur_enabled": "Unschärfe aktiviert",
        "blur_disabled": "Unschärfe deaktiviert",
        "blur_type_set": "Unschärfetyp: {}",
        "blur_opacity_set": "Unschärfeopazität: {}",
        "blur_intensity_set": "Unschärfeintensität: {}",
        "tint_opacity_set": "Tönungsopazität: {}",
        "changes_undone": "Änderungen rückgängig gemacht",
        "nothing_to_undo": "Nichts rückgängig zu machen",
        "reset_complete": "Fenster auf ursprünglichen Zustand zurückgesetzt",
        "profile_saved": "Profil gespeichert",
        "profile_loaded": "Profil geladen",
        "profile_error": "Fehler beim Verarbeiten des Profils",
        "language": "Sprache",
        "error": "Fehler",
        "window_incompatible": "Dieses Fenster unterstützt keine Unschärfeeffekte",
        "tooltip_refresh": "Liste der aktiven Fenster aktualisieren",
        "tooltip_auto_refresh": "Fensterliste automatisch aktualisieren",
        "tooltip_transparency": "Fenstertransparenz anpassen (50-255)",
        "tooltip_enable_blur": "Unschärfeeffekt aktivieren oder deaktivieren",
        "tooltip_blur_type": "Zwischen Standard- und Acrylunschärfe wählen",
        "tooltip_blur_opacity": "Unschärfeopazität anpassen (0-255)",
        "tooltip_blur_intensity": "Unschärfeintensität anpassen (0-100)",
        "tooltip_tint_opacity": "Tönungsopazität des Hintergrunds anpassen (0-255)",
        "tooltip_undo": "Letzte Änderung rückgängig machen",
        "tooltip_reset": "Fenster auf ursprünglichen Zustand zurücksetzen",
        "tooltip_save_profile": "Aktuelle Einstellungen als Profil speichern",
        "tooltip_load_profile": "Gespeichertes Profil laden",
        "tooltip_language": "Anwendungssprache wählen",
        "tooltip_about": "Informationen über das Programm anzeigen"
    },
    "es": {
        "title": "Desenfoque Personalizado",
        "windows": "Ventanas",
        "refresh": "🔄 Actualizar",
        "auto_refresh": "Actualización automática",
        "transparency": "Transparencia",
        "blur_effect": "Efecto de Desenfoque",
        "enable_blur": "Activar Desenfoque",
        "blur_type": ["Desenfoque Estándar", "Desenfoque Acrílico"],
        "blur_opacity": "Opacidad de Desenfoque",
        "blur_intensity": "Intensidad de Desenfoque",
        "tint_opacity": "Opacidad de Tinte",
        "undo": "⟲ Deshacer",
        "reset": "🔄 Restablecer",
        "about": "Acerca de",
        "save_profile": "Guardar Perfil",
        "load_profile": "Cargar Perfil",
        "ready": "Listo",
        "window_list_refreshed": "Lista de ventanas actualizada",
        "selected": "Seleccionado: {}",
        "window_not_found": "¡Ventana no encontrada!",
        "transparency_set": "Transparencia: {}",
        "blur_enabled": "Desenfoque activado",
        "blur_disabled": "Desenfoque desactivado",
        "blur_type_set": "Tipo de desenfoque: {}",
        "blur_opacity_set": "Opacidad de desenfoque: {}",
        "blur_intensity_set": "Intensidad de desenfoque: {}",
        "tint_opacity_set": "Opacidad de tinte: {}",
        "changes_undone": "Cambios deshechos",
        "nothing_to_undo": "Nada que deshacer",
        "reset_complete": "Ventana restablecida a su estado original",
        "profile_saved": "Perfil guardado",
        "profile_loaded": "Perfil cargado",
        "profile_error": "Error al procesar el perfil",
        "language": "Idioma",
        "error": "Error",
        "window_incompatible": "Esta ventana no admite efectos de desenfoque",
        "tooltip_refresh": "Actualizar la lista de ventanas activas",
        "tooltip_auto_refresh": "Actualizar automáticamente la lista de ventanas",
        "tooltip_transparency": "Ajustar la transparencia de la ventana (50-255)",
        "tooltip_enable_blur": "Activar o desactivar el efecto de desenfoque",
        "tooltip_blur_type": "Elegir entre desenfoque estándar o acrílico",
        "tooltip_blur_opacity": "Ajustar la opacidad del desenfoque (0-255)",
        "tooltip_blur_intensity": "Ajustar la intensidad del desenfoque (0-100)",
        "tooltip_tint_opacity": "Ajustar la opacidad del tinte de fondo (0-255)",
        "tooltip_undo": "Deshacer el último cambio",
        "tooltip_reset": "Restablecer la ventana a su estado original",
        "tooltip_save_profile": "Guardar la configuración actual como perfil",
        "tooltip_load_profile": "Cargar un perfil guardado",
        "tooltip_language": "Seleccionar el idioma de la aplicación",
        "tooltip_about": "Ver información sobre el programa"
    },
    "fr": {
        "title": "Flou Personnalisé",
        "windows": "Fenêtres",
        "refresh": "🔄 Actualiser",
        "auto_refresh": "Actualisation automatique",
        "transparency": "Transparence",
        "blur_effect": "Effet de Flou",
        "enable_blur": "Activer le Flou",
        "blur_type": ["Flou Standard", "Flou Acrylique"],
        "blur_opacity": "Opacité du Flou",
        "blur_intensity": "Intensité du Flou",
        "tint_opacity": "Opacité de la Teinte",
        "undo": "⟲ Annuler",
        "reset": "🔄 Réinitialiser",
        "about": "À propos",
        "save_profile": "Enregistrer le Profil",
        "load_profile": "Charger le Profil",
        "ready": "Prêt",
        "window_list_refreshed": "Liste des fenêtres actualisée",
        "selected": "Sélectionné : {}",
        "window_not_found": "Fenêtre non trouvée !",
        "transparency_set": "Transparence : {}",
        "blur_enabled": "Flou activé",
        "blur_disabled": "Flou désactivé",
        "blur_type_set": "Type de flou : {}",
        "blur_opacity_set": "Opacité du flou : {}",
        "blur_intensity_set": "Intensité du flou : {}",
        "tint_opacity_set": "Opacité de la teinte : {}",
        "changes_undone": "Modifications annulées",
        "nothing_to_undo": "Rien à annuler",
        "reset_complete": "Fenêtre réinitialisée à son état initial",
        "profile_saved": "Profil enregistré",
        "profile_loaded": "Profil chargé",
        "profile_error": "Erreur lors du traitement du profil",
        "language": "Langue",
        "error": "Erreur",
        "window_incompatible": "Cette fenêtre ne prend pas en charge les effets de flou",
        "tooltip_refresh": "Actualiser la liste des fenêtres actives",
        "tooltip_auto_refresh": "Actualiser automatiquement la liste des fenêtres",
        "tooltip_transparency": "Ajuster la transparence de la fenêtre (50-255)",
        "tooltip_enable_blur": "Activer ou désactiver l'effet de flou",
        "tooltip_blur_type": "Choisir entre un flou standard ou acrylique",
        "tooltip_blur_opacity": "Ajuster l'opacité du flou (0-255)",
        "tooltip_blur_intensity": "Ajuster l'intensité du flou (0-100)",
        "tooltip_tint_opacity": "Ajuster l'opacité de la teinte de fond (0-255)",
        "tooltip_undo": "Annuler la dernière modification",
        "tooltip_reset": "Réinitialiser la fenêtre à son état initial",
        "tooltip_save_profile": "Enregistrer les paramètres actuels comme profil",
        "tooltip_load_profile": "Charger un profil enregistré",
        "tooltip_language": "Sélectionner la langue de l'application",
        "tooltip_about": "Voir les informations sur le programme"
    }
}

def make_window_transparent(hwnd, alpha=255):
    try:
        styles = GetWindowLong(hwnd, GWL_EXSTYLE)
        if not styles:
            return False
        SetWindowLong(hwnd, GWL_EXSTYLE, styles | WS_EX_LAYERED)
        SetLayeredWindowAttributes(hwnd, 0, alpha, LWA_ALPHA)
        return True
    except Exception as e:
        logging.error(f"Error setting transparency: {e}")
        return False

def enable_blur(hwnd, blur_type=ACCENT_ENABLE_BLURBEHIND, opacity=0, intensity=0):
    try:
        gradient_color = (opacity << 24) | 0x000000
        accent = ACCENT_POLICY()
        accent.AccentState = blur_type
        accent.AccentFlags = 0
        accent.GradientColor = gradient_color
        accent.AnimationId = 0

        data = WINDOWCOMPOSITIONATTRIBDATA()
        data.Attribute = WCA_ACCENT_POLICY
        data.Data = ctypes.addressof(accent)
        data.SizeOfData = ctypes.sizeof(accent)

        result = SetWindowCompositionAttribute(hwnd, ctypes.byref(data))
        if not result:
            return False
        return True
    except Exception as e:
        logging.error(f"Error enabling blur: {e}")
        return False

def disable_blur(hwnd, original_styles, original_alpha):
    try:
        accent = ACCENT_POLICY()
        accent.AccentState = 0
        accent.AccentFlags = 0
        accent.GradientColor = 0
        accent.AnimationId = 0

        data = WINDOWCOMPOSITIONATTRIBDATA()
        data.Attribute = WCA_ACCENT_POLICY
        data.Data = ctypes.addressof(accent)
        data.SizeOfData = ctypes.sizeof(accent)

        SetWindowCompositionAttribute(hwnd, ctypes.byref(data))
        SetWindowLong(hwnd, GWL_EXSTYLE, original_styles)
        if original_styles & WS_EX_LAYERED:
            SetLayeredWindowAttributes(hwnd, 0, original_alpha, LWA_ALPHA)
        else:
            SetLayeredWindowAttributes(hwnd, 0, 255, LWA_ALPHA)
        return True
    except Exception as e:
        logging.error(f"Error disabling blur: {e}")
        return False

def is_dwm_composition_enabled():
    try:
        enabled = ctypes.c_bool()
        dwmapi.DwmIsCompositionEnabled(ctypes.byref(enabled))
        return enabled.value
    except Exception as e:
        logging.error(f"Error checking DWM composition: {e}")
        return False

class Tooltip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tip_window = None
        self.id = None
        self.x = self.y = 0
        self.widget.bind("<Enter>", self.show_tip)
        self.widget.bind("<Leave>", self.hide_tip)

    def show_tip(self, event):
        self.x = event.x_root + 10
        self.y = event.y_root + 10
        self.tip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{self.x}+{self.y}")
        label = tk.Label(tw, text=self.text, justify=tk.LEFT, bg="#333333", fg="white", relief=tk.SOLID, borderwidth=1, font=("Roboto", 10))
        label.pack()

    def hide_tip(self, event):
        if self.tip_window:
            self.tip_window.destroy()
        self.tip_window = None

class CustomBlurApp:
    def __init__(self, root):
        self.root = root
        self.language = self.load_language()
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        root.title(LOCALIZATION[self.language]["title"])
        root.geometry("800x600")
        root.resizable(False, False)

        self.selected_hwnd = None
        self.history = {}
        self.original_states = {}
        self.max_history = 20
        self.window_list = []
        self.profiles = self.load_profiles()

        self.main_frame = ctk.CTkFrame(root, corner_radius=0, fg_color="#1a1a1a")
        self.main_frame.pack(fill="both", expand=True)

        self.top_bar = ctk.CTkFrame(self.main_frame, corner_radius=0, fg_color="#2b2b2b")
        self.top_bar.pack(side="top", fill="x")

        self.about_button = ctk.CTkButton(self.top_bar, text=LOCALIZATION[self.language]["about"], command=self.show_about, width=100, fg_color="#3a3a3a", hover_color="#4a4a4a")
        self.about_button.pack(side="left", padx=10, pady=5)
        Tooltip(self.about_button, LOCALIZATION[self.language]["tooltip_about"])

        self.sidebar = ctk.CTkFrame(self.main_frame, width=300, corner_radius=0, fg_color="#2b2b2b")
        self.sidebar.pack(side="left", fill="y", padx=(0, 1))

        self.title_label = ctk.CTkLabel(self.sidebar, text=LOCALIZATION[self.language]["title"], font=("Roboto", 18, "bold"), text_color="#ffffff")
        self.title_label.pack(pady=20)

        self.language_label = ctk.CTkLabel(self.sidebar, text=LOCALIZATION[self.language]["language"], font=("Roboto", 12), text_color="#cccccc")
        self.language_label.pack(pady=10, padx=10, anchor="w")
        self.language_menu = ctk.CTkOptionMenu(
            self.sidebar,
            values=["English", "Русский", "Українська", "Беларуская", "Deutsch", "Español", "Français"],
            command=self.change_language,
            fg_color="#3a3a3a",
            button_color="#4a4a4a",
            button_hover_color="#5a5a5a"
        )
        self.language_menu.set({
            "en": "English",
            "ru": "Русский",
            "uk": "Українська",
            "be": "Беларуская",
            "de": "Deutsch",
            "es": "Español",
            "fr": "Français"
        }[self.language])
        self.language_menu.pack(pady=5, padx=10)
        Tooltip(self.language_menu, LOCALIZATION[self.language]["tooltip_language"])

        self.window_label = ctk.CTkLabel(self.sidebar, text=LOCALIZATION[self.language]["windows"], font=("Roboto", 12), text_color="#cccccc")
        self.window_label.pack(pady=10, padx=10, anchor="w")

        self.window_frame = ctk.CTkScrollableFrame(self.sidebar, height=300, width=280, fg_color="#333333")
        self.window_frame.pack(padx=10, pady=5)

        self.window_listbox = tk.Listbox(
            self.window_frame,
            height=15,
            width=40,
            font=("Roboto", 12),
            bg="#333333",
            fg="white",
            selectbackground="#1f6aa5",
            selectforeground="white",
            highlightthickness=0,
            borderwidth=0
        )
        self.window_listbox.pack(fill="both", expand=True)
        self.window_listbox.bind("<<ListboxSelect>>", self.select_window)

        self.refresh_button = ctk.CTkButton(self.sidebar, text=LOCALIZATION[self.language]["refresh"], command=self.refresh_list, width=100, fg_color="#3a3a3a", hover_color="#4a4a4a")
        self.refresh_button.pack(pady=10)
        Tooltip(self.refresh_button, LOCALIZATION[self.language]["tooltip_refresh"])

        self.auto_refresh_toggle = ctk.CTkSwitch(self.sidebar, text=LOCALIZATION[self.language]["auto_refresh"], command=self.toggle_auto_refresh, fg_color="#3a3a3a", progress_color="#1f6aa5")
        self.auto_refresh_toggle.pack(pady=5)
        Tooltip(self.auto_refresh_toggle, LOCALIZATION[self.language]["tooltip_auto_refresh"])
        self.auto_refresh_interval = 5000
        self.auto_refresh_id = None

        self.controls_frame = ctk.CTkFrame(self.main_frame, corner_radius=15, fg_color="#2b2b2b")
        self.controls_frame.pack(side="right", fill="both", expand=True, padx=20, pady=20)

        self.trans_label = ctk.CTkLabel(self.controls_frame, text=LOCALIZATION[self.language]["transparency"], font=("Roboto", 14), text_color="#cccccc")
        self.trans_label.pack(pady=10)
        self.transparency_scale = ctk.CTkSlider(self.controls_frame, from_=50, to=255, command=self.update_transparency, button_color="#1f6aa5", progress_color="#1f6aa5")
        self.transparency_scale.set(255)
        self.transparency_scale.pack(pady=5, padx=20)
        Tooltip(self.transparency_scale, LOCALIZATION[self.language]["tooltip_transparency"])

        self.blur_label = ctk.CTkLabel(self.controls_frame, text=LOCALIZATION[self.language]["blur_effect"], font=("Roboto", 14), text_color="#cccccc")
        self.blur_label.pack(pady=10)
        self.blur_toggle = ctk.CTkSwitch(self.controls_frame, text=LOCALIZATION[self.language]["enable_blur"], command=self.toggle_blur, fg_color="#3a3a3a", progress_color="#1f6aa5")
        self.blur_toggle.pack(pady=5)
        Tooltip(self.blur_toggle, LOCALIZATION[self.language]["tooltip_enable_blur"])

        self.blur_type = ctk.CTkOptionMenu(self.controls_frame, values=LOCALIZATION[self.language]["blur_type"], command=self.update_blur_type, fg_color="#3a3a3a", button_color="#4a4a4a", button_hover_color="#5a5a5a")
        self.blur_type.pack(pady=5)
        Tooltip(self.blur_type, LOCALIZATION[self.language]["tooltip_blur_type"])

        self.blur_opacity_label = ctk.CTkLabel(self.controls_frame, text=LOCALIZATION[self.language]["blur_opacity"], font=("Roboto", 12), text_color="#cccccc")
        self.blur_opacity_label.pack(pady=5)
        self.blur_opacity_scale = ctk.CTkSlider(self.controls_frame, from_=0, to=255, command=self.update_blur_opacity, button_color="#1f6aa5", progress_color="#1f6aa5")
        self.blur_opacity_scale.set(0)
        self.blur_opacity_scale.pack(pady=5, padx=20)
        Tooltip(self.blur_opacity_scale, LOCALIZATION[self.language]["tooltip_blur_opacity"])

        self.blur_intensity_label = ctk.CTkLabel(self.controls_frame, text=LOCALIZATION[self.language]["blur_intensity"], font=("Roboto", 12), text_color="#cccccc")
        self.blur_intensity_label.pack(pady=5)
        self.blur_intensity_scale = ctk.CTkSlider(self.controls_frame, from_=0, to=100, command=self.update_blur_intensity, button_color="#1f6aa5", progress_color="#1f6aa5")
        self.blur_intensity_scale.set(0)
        self.blur_intensity_scale.pack(pady=5, padx=20)
        Tooltip(self.blur_intensity_scale, LOCALIZATION[self.language]["tooltip_blur_intensity"])

        self.tint_opacity_label = ctk.CTkLabel(self.controls_frame, text=LOCALIZATION[self.language]["tint_opacity"], font=("Roboto", 12), text_color="#cccccc")
        self.tint_opacity_label.pack(pady=5)
        self.tint_opacity_scale = ctk.CTkSlider(self.controls_frame, from_=0, to=255, command=self.update_tint_opacity, button_color="#1f6aa5", progress_color="#1f6aa5")
        self.tint_opacity_scale.set(0)
        self.tint_opacity_scale.pack(pady=5, padx=20)
        Tooltip(self.tint_opacity_scale, LOCALIZATION[self.language]["tooltip_tint_opacity"])

        self.profile_frame = ctk.CTkFrame(self.controls_frame, corner_radius=10, fg_color="#333333")
        self.profile_frame.pack(pady=10, padx=10, fill="x")
        self.save_profile_button = ctk.CTkButton(self.profile_frame, text=LOCALIZATION[self.language]["save_profile"], command=self.save_profile, width=100, fg_color="#3a3a3a", hover_color="#4a4a4a")
        self.save_profile_button.pack(side="left", padx=5)
        Tooltip(self.save_profile_button, LOCALIZATION[self.language]["tooltip_save_profile"])
        self.load_profile_button = ctk.CTkButton(self.profile_frame, text=LOCALIZATION[self.language]["load_profile"], command=self.load_profile, width=100, fg_color="#3a3a3a", hover_color="#4a4a4a")
        self.load_profile_button.pack(side="left", padx=5)
        Tooltip(self.load_profile_button, LOCALIZATION[self.language]["tooltip_load_profile"])

        self.action_frame = ctk.CTkFrame(self.controls_frame, corner_radius=10, fg_color="#333333")
        self.action_frame.pack(pady=10, padx=10, fill="x")
        self.undo_button = ctk.CTkButton(self.action_frame, text=LOCALIZATION[self.language]["undo"], command=self.undo, width=100, fg_color="#3a3a3a", hover_color="#4a4a4a")
        self.undo_button.pack(side="left", padx=5)
        Tooltip(self.undo_button, LOCALIZATION[self.language]["tooltip_undo"])
        self.reset_button = ctk.CTkButton(self.action_frame, text=LOCALIZATION[self.language]["reset"], command=self.reset_window, width=100, fg_color="#3a3a3a", hover_color="#4a4a4a")
        self.reset_button.pack(side="left", padx=5)
        Tooltip(self.reset_button, LOCALIZATION[self.language]["tooltip_reset"])

        self.status = ctk.CTkLabel(self.controls_frame, text=LOCALIZATION[self.language]["ready"], font=("Roboto", 12), text_color="#cccccc")
        self.status.pack(pady=10)

        self.refresh_list()
        if self.auto_refresh_toggle.get():
            self.start_auto_refresh()

    def load_language(self):
        config_file = "blur_config.json"
        default_language = "en"
        try:
            if os.path.exists(config_file):
                with open(config_file, "r", encoding="utf-8") as f:
                    config = json.load(f)
                    return config.get("language", default_language)
        except Exception as e:
            logging.error(f"Error loading language: {e}")
        return default_language

    def save_language(self):
        config_file = "blur_config.json"
        try:
            config = {"language": self.language}
            with open(config_file, "w", encoding="utf-8") as f:
                json.dump(config, f)
        except Exception as e:
            logging.error(f"Error saving language: {e}")

    def load_profiles(self):
        profiles_file = "blur_profiles.json"
        try:
            if os.path.exists(profiles_file):
                with open(profiles_file, "r", encoding="utf-8") as f:
                    return json.load(f)
        except Exception as e:
            logging.error(f"Error loading profiles: {e}")
        return {}

    def save_profiles(self):
        profiles_file = "blur_profiles.json"
        try:
            with open(profiles_file, "w", encoding="utf-8") as f:
                json.dump(self.profiles, f)
        except Exception as e:
            logging.error(f"Error saving profiles: {e}")

    def change_language(self, language_name):
        language_map = {
            "English": "en",
            "Русский": "ru",
            "Українська": "uk",
            "Беларуская": "be",
            "Deutsch": "de",
            "Español": "es",
            "Français": "fr"
        }
        self.language = language_map[language_name]
        self.save_language()
        self.update_ui_texts()

    def show_about(self):
        about_dialog = ctk.CTkToplevel(self.root)
        about_dialog.title(LOCALIZATION[self.language]["about"])
        about_dialog.geometry("400x250")
        about_dialog.resizable(False, False)

        title = ctk.CTkLabel(about_dialog, text="Custom Blur", font=("Roboto", 16, "bold"), text_color="#ffffff")
        title.pack(pady=20)

        version = ctk.CTkLabel(about_dialog, text="Version: 0.0.1", font=("Roboto", 12), text_color="#cccccc")
        version.pack(pady=5)

        developer = ctk.CTkLabel(about_dialog, text="Developer: Scody", font=("Roboto", 12), text_color="#cccccc")
        developer.pack(pady=5)

        github = ctk.CTkLabel(about_dialog, text="GitHub: https://github.com/Scody0", font=("Roboto", 12), text_color="#1f6aa5")
        github.pack(pady=5)

        close_button = ctk.CTkButton(about_dialog, text="Close", command=about_dialog.destroy, width=100, fg_color="#3a3a3a", hover_color="#4a4a4a")
        close_button.pack(pady=20)

    def update_ui_texts(self):
        try:
            self.root.title(LOCALIZATION[self.language]["title"])
            self.title_label.configure(text=LOCALIZATION[self.language]["title"])
            self.language_label.configure(text=LOCALIZATION[self.language]["language"])
            self.window_label.configure(text=LOCALIZATION[self.language]["windows"])
            self.refresh_button.configure(text=LOCALIZATION[self.language]["refresh"])
            self.auto_refresh_toggle.configure(text=LOCALIZATION[self.language]["auto_refresh"])
            self.trans_label.configure(text=LOCALIZATION[self.language]["transparency"])
            self.blur_label.configure(text=LOCALIZATION[self.language]["blur_effect"])
            self.blur_toggle.configure(text=LOCALIZATION[self.language]["enable_blur"])
            self.blur_type.configure(values=LOCALIZATION[self.language]["blur_type"])
            self.blur_type.set(LOCALIZATION[self.language]["blur_type"][0])
            self.blur_opacity_label.configure(text=LOCALIZATION[self.language]["blur_opacity"])
            self.blur_intensity_label.configure(text=LOCALIZATION[self.language]["blur_intensity"])
            self.tint_opacity_label.configure(text=LOCALIZATION[self.language]["tint_opacity"])
            self.save_profile_button.configure(text=LOCALIZATION[self.language]["save_profile"])
            self.load_profile_button.configure(text=LOCALIZATION[self.language]["load_profile"])
            self.undo_button.configure(text=LOCALIZATION[self.language]["undo"])
            self.reset_button.configure(text=LOCALIZATION[self.language]["reset"])
            self.about_button.configure(text=LOCALIZATION[self.language]["about"])
            self.status.configure(text=LOCALIZATION[self.language]["ready"])
        except Exception as e:
            logging.error(f"Error updating UI texts: {e}")

    def toggle_auto_refresh(self):
        if self.auto_refresh_toggle.get():
            self.start_auto_refresh()
        else:
            self.stop_auto_refresh()

    def start_auto_refresh(self):
        self.refresh_list()
        self.auto_refresh_id = self.root.after(self.auto_refresh_interval, self.start_auto_refresh)

    def stop_auto_refresh(self):
        if self.auto_refresh_id:
            self.root.after_cancel(self.auto_refresh_id)
            self.auto_refresh_id = None

    def refresh_list(self):
        try:
            self.window_listbox.delete(0, tk.END)
            self.window_list = []
            windows = gw.getAllWindows()
            for window in windows:
                if window.title and window.visible and not window.isMinimized:
                    self.window_list.append(window.title)
                    self.window_listbox.insert(tk.END, window.title)
            self.status.configure(text=LOCALIZATION[self.language]["window_list_refreshed"])
        except Exception as e:
            logging.error(f"Error refreshing window list: {e}")
            self.status.configure(text=LOCALIZATION[self.language]["error"])

    def select_window(self, event=None):
        try:
            selection_index = self.window_listbox.curselection()
            if not selection_index:
                return
            selection = self.window_listbox.get(selection_index[0]).strip()
            window = gw.getWindowsWithTitle(selection)[0]
            self.selected_hwnd = window._hWnd

            styles = GetWindowLong(self.selected_hwnd, GWL_EXSTYLE)
            alpha = 255
            if styles & WS_EX_LAYERED:
                alpha = 255
            self.original_states[self.selected_hwnd] = (styles, alpha)

            if self.selected_hwnd not in self.history:
                self.history[self.selected_hwnd] = deque(maxlen=self.max_history)
                self.save_settings({
                    'transparency': 255,
                    'blur': False,
                    'blur_type': LOCALIZATION[self.language]["blur_type"][0],
                    'blur_opacity': 0,
                    'blur_intensity': 0,
                    'tint_opacity': 0
                })
            self.status.configure(text=LOCALIZATION[self.language]["selected"].format(selection))
            self.apply_settings(self.history[self.selected_hwnd][-1])
        except IndexError:
            self.status.configure(text=LOCALIZATION[self.language]["window_not_found"])
        except Exception as e:
            logging.error(f"Error selecting window: {e}")
            self.status.configure(text=LOCALIZATION[self.language]["error"])

    def update_transparency(self, value):
        if self.selected_hwnd:
            try:
                alpha = int(value)
                if make_window_transparent(self.selected_hwnd, alpha):
                    self.save_settings({'transparency': alpha})
                    self.status.configure(text=LOCALIZATION[self.language]["transparency_set"].format(alpha))
                else:
                    self.status.configure(text=LOCALIZATION[self.language]["error"])
            except Exception as e:
                logging.error(f"Error updating transparency: {e}")
                self.status.configure(text=LOCALIZATION[self.language]["error"])

    def toggle_blur(self):
        if self.selected_hwnd:
            try:
                state = self.blur_toggle.get()
                settings = {'blur': state}
                if state:
                    if not is_dwm_composition_enabled():
                        messagebox.showerror(LOCALIZATION[self.language]["error"], LOCALIZATION[self.language]["window_incompatible"])
                        self.blur_toggle.deselect()
                        return
                    blur_type = ACCENT_ENABLE_ACRYLICBLURBEHIND if self.blur_type.get() == LOCALIZATION[self.language]["blur_type"][1] else ACCENT_ENABLE_BLURBEHIND
                    opacity = int(self.blur_opacity_scale.get())
                    intensity = int(self.blur_intensity_scale.get())
                    if enable_blur(self.selected_hwnd, blur_type, opacity, intensity):
                        settings.update({
                            'blur_type': self.blur_type.get(),
                            'blur_opacity': opacity,
                            'blur_intensity': intensity,
                            'tint_opacity': int(self.tint_opacity_scale.get())
                        })
                        self.status.configure(text=LOCALIZATION[self.language]["blur_enabled"])
                    else:
                        messagebox.showerror(LOCALIZATION[self.language]["error"], LOCALIZATION[self.language]["window_incompatible"])
                        self.blur_toggle.deselect()
                else:
                    original_styles, original_alpha = self.original_states.get(self.selected_hwnd, (0, 255))
                    if disable_blur(self.selected_hwnd, original_styles, original_alpha):
                        self.status.configure(text=LOCALIZATION[self.language]["blur_disabled"])
                    else:
                        self.status.configure(text=LOCALIZATION[self.language]["error"])
                self.save_settings(settings)
            except Exception as e:
                logging.error(f"Error toggling blur: {e}")
                self.status.configure(text=LOCALIZATION[self.language]["error"])

    def update_blur_type(self, value):
        if self.selected_hwnd and self.blur_toggle.get():
            try:
                blur_type = ACCENT_ENABLE_ACRYLICBLURBEHIND if value == LOCALIZATION[self.language]["blur_type"][1] else ACCENT_ENABLE_BLURBEHIND
                opacity = int(self.blur_opacity_scale.get())
                intensity = int(self.blur_intensity_scale.get())
                if enable_blur(self.selected_hwnd, blur_type, opacity, intensity):
                    self.save_settings({
                        'blur_type': value,
                        'blur_opacity': opacity,
                        'blur_intensity': intensity,
                        'tint_opacity': int(self.tint_opacity_scale.get())
                    })
                    self.status.configure(text=LOCALIZATION[self.language]["blur_type_set"].format(value))
                else:
                    self.status.configure(text=LOCALIZATION[self.language]["error"])
            except Exception as e:
                logging.error(f"Error updating blur type: {e}")
                self.status.configure(text=LOCALIZATION[self.language]["error"])

    def update_blur_opacity(self, value):
        if self.selected_hwnd and self.blur_toggle.get():
            try:
                opacity = int(value)
                blur_type = ACCENT_ENABLE_ACRYLICBLURBEHIND if self.blur_type.get() == LOCALIZATION[self.language]["blur_type"][1] else ACCENT_ENABLE_BLURBEHIND
                intensity = int(self.blur_intensity_scale.get())
                if enable_blur(self.selected_hwnd, blur_type, opacity, intensity):
                    self.save_settings({
                        'blur_opacity': opacity,
                        'blur_intensity': intensity,
                        'tint_opacity': int(self.tint_opacity_scale.get())
                    })
                    self.status.configure(text=LOCALIZATION[self.language]["blur_opacity_set"].format(opacity))
                else:
                    self.status.configure(text=LOCALIZATION[self.language]["error"])
            except Exception as e:
                logging.error(f"Error updating blur opacity: {e}")
                self.status.configure(text=LOCALIZATION[self.language]["error"])

    def update_blur_intensity(self, value):
        if self.selected_hwnd and self.blur_toggle.get():
            try:
                intensity = int(value)
                blur_type = ACCENT_ENABLE_ACRYLICBLURBEHIND if self.blur_type.get() == LOCALIZATION[self.language]["blur_type"][1] else ACCENT_ENABLE_BLURBEHIND
                opacity = int(self.blur_opacity_scale.get())
                if enable_blur(self.selected_hwnd, blur_type, opacity, intensity):
                    self.save_settings({
                        'blur_intensity': intensity,
                        'blur_opacity': opacity,
                        'tint_opacity': int(self.tint_opacity_scale.get())
                    })
                    self.status.configure(text=LOCALIZATION[self.language]["blur_intensity_set"].format(intensity))
                else:
                    self.status.configure(text=LOCALIZATION[self.language]["error"])
            except Exception as e:
                logging.error(f"Error updating blur intensity: {e}")
                self.status.configure(text=LOCALIZATION[self.language]["error"])

    def update_tint_opacity(self, value):
        if self.selected_hwnd and self.blur_toggle.get():
            try:
                tint_opacity = int(value)
                blur_type = ACCENT_ENABLE_ACRYLICBLURBEHIND if self.blur_type.get() == LOCALIZATION[self.language]["blur_type"][1] else ACCENT_ENABLE_BLURBEHIND
                opacity = int(self.blur_opacity_scale.get())
                intensity = int(self.blur_intensity_scale.get())
                if enable_blur(self.selected_hwnd, blur_type, opacity, intensity):
                    self.save_settings({
                        'tint_opacity': tint_opacity,
                        'blur_opacity': opacity,
                        'blur_intensity': intensity
                    })
                    self.status.configure(text=LOCALIZATION[self.language]["tint_opacity_set"].format(tint_opacity))
                else:
                    self.status.configure(text=LOCALIZATION[self.language]["error"])
            except Exception as e:
                logging.error(f"Error updating tint opacity: {e}")
                self.status.configure(text=LOCALIZATION[self.language]["error"])

    def save_profile(self):
        if self.selected_hwnd:
            try:
                profile_name = tk.simpledialog.askstring("Save Profile", "Enter profile name:")
                if profile_name:
                    window_title = self.window_listbox.get(self.window_listbox.curselection()[0]).strip()
                    self.profiles[profile_name] = {
                        'window_title': window_title,
                        'settings': self.history[self.selected_hwnd][-1]
                    }
                    self.save_profiles()
                    self.status.configure(text=LOCALIZATION[self.language]["profile_saved"])
            except Exception as e:
                logging.error(f"Error saving profile: {e}")
                self.status.configure(text=LOCALIZATION[self.language]["profile_error"])

    def load_profile(self):
        if self.selected_hwnd:
            try:
                profile_names = list(self.profiles.keys())
                if not profile_names:
                    self.status.configure(text=LOCALIZATION[self.language]["profile_error"])
                    return
                profile_name = tk.StringVar()
                dialog = ctk.CTkToplevel(self.root)
                dialog.title("Load Profile")
                dialog.geometry("300x150")
                ctk.CTkLabel(dialog, text="Select Profile:", font=("Roboto", 12)).pack(pady=10)
                profile_menu = ctk.CTkOptionMenu(dialog, values=profile_names, variable=profile_name)
                profile_menu.pack(pady=5)
                ctk.CTkButton(dialog, text="Load", command=lambda: self.apply_profile(profile_name.get(), dialog)).pack(pady=10)
            except Exception as e:
                logging.error(f"Error loading profile: {e}")
                self.status.configure(text=LOCALIZATION[self.language]["profile_error"])

    def apply_profile(self, profile_name, dialog):
        try:
            profile = self.profiles.get(profile_name)
            if not profile:
                self.status.configure(text=LOCALIZATION[self.language]["profile_error"])
                return
            window_title = profile['window_title']
            settings = profile['settings']
            windows = gw.getWindowsWithTitle(window_title)
            if not windows:
                self.status.configure(text=LOCALIZATION[self.language]["window_not_found"])
                return
            self.selected_hwnd = windows[0]._hWnd
            self.history[self.selected_hwnd] = deque(maxlen=self.max_history)
            self.history[self.selected_hwnd].append(settings)
            self.apply_settings(settings)
            self.status.configure(text=LOCALIZATION[self.language]["profile_loaded"])
            dialog.destroy()
        except Exception as e:
            logging.error(f"Error applying profile: {e}")
            self.status.configure(text=LOCALIZATION[self.language]["profile_error"])

    def save_settings(self, settings):
        if self.selected_hwnd:
            try:
                current = self.history[self.selected_hwnd][-1].copy() if self.history[self.selected_hwnd] else {
                    'transparency': 255,
                    'blur': False,
                    'blur_type': LOCALIZATION[self.language]["blur_type"][0],
                    'blur_opacity': 0,
                    'blur_intensity': 0,
                    'tint_opacity': 0
                }
                current.update(settings)
                self.history[self.selected_hwnd].append(current)
            except Exception as e:
                logging.error(f"Error saving settings: {e}")
                self.status.configure(text=LOCALIZATION[self.language]["error"])

    def undo(self):
        if self.selected_hwnd and len(self.history[self.selected_hwnd]) > 1:
            try:
                self.history[self.selected_hwnd].pop()
                settings = self.history[self.selected_hwnd][-1]
                self.apply_settings(settings)
                self.status.configure(text=LOCALIZATION[self.language]["changes_undone"])
            except Exception as e:
                logging.error(f"Error undoing changes: {e}")
                self.status.configure(text=LOCALIZATION[self.language]["error"])
        else:
            self.status.configure(text=LOCALIZATION[self.language]["nothing_to_undo"])

    def reset_window(self):
        if self.selected_hwnd:
            try:
                original_styles, original_alpha = self.original_states.get(self.selected_hwnd, (0, 255))
                if disable_blur(self.selected_hwnd, original_styles, original_alpha):
                    self.history[self.selected_hwnd].clear()
                    self.save_settings({
                        'transparency': 255,
                        'blur': False,
                        'blur_type': LOCALIZATION[self.language]["blur_type"][0],
                        'blur_opacity': 0,
                        'blur_intensity': 0,
                        'tint_opacity': 0
                    })
                    self.apply_settings(self.history[self.selected_hwnd][-1])
                    self.status.configure(text=LOCALIZATION[self.language]["reset_complete"])
                else:
                    self.status.configure(text=LOCALIZATION[self.language]["error"])
            except Exception as e:
                logging.error(f"Error resetting window: {e}")
                self.status.configure(text=LOCALIZATION[self.language]["error"])

    def apply_settings(self, settings):
        try:
            self.transparency_scale.set(settings['transparency'])
            self.blur_toggle.deselect() if not settings['blur'] else self.blur_toggle.select()
            self.blur_type.set(settings['blur_type'])
            self.blur_opacity_scale.set(settings['blur_opacity'])
            self.blur_intensity_scale.set(settings['blur_intensity'])
            self.tint_opacity_scale.set(settings['tint_opacity'])

            if self.selected_hwnd:
                make_window_transparent(self.selected_hwnd, settings['transparency'])
                if settings['blur']:
                    blur_type = ACCENT_ENABLE_ACRYLICBLURBEHIND if settings['blur_type'] == LOCALIZATION[self.language]["blur_type"][1] else ACCENT_ENABLE_BLURBEHIND
                    enable_blur(self.selected_hwnd, blur_type, settings['blur_opacity'], settings['blur_intensity'])
                else:
                    original_styles, original_alpha = self.original_states.get(self.selected_hwnd, (0, 255))
                    disable_blur(self.selected_hwnd, original_styles, original_alpha)
        except Exception as e:
            logging.error(f"Error applying settings: {e}")
            self.status.configure(text=LOCALIZATION[self.language]["error"])

if __name__ == "__main__":
    root = ctk.CTk()
    app = CustomBlurApp(root)
    root.mainloop()
