cat > templates/index.json <<'DBEOF'
{
 "sections": {
  "hero_db": {
   "type": "hero",
   "blocks": {
    "hero_t1": {
     "type": "text",
     "settings": {
      "text": "<h1>Neue Saison, neue Styles</h1>",
      "type_preset": "h1",
      "alignment": "center",
      "width": "100%"
     }
    },
    "hero_t2": {
     "type": "text",
     "settings": {
      "text": "<p>Entdecken Sie jetzt unsere aktuelle Kollektion für die laufende Saison.</p>",
      "type_preset": "rte",
      "alignment": "center",
      "width": "100%"
     }
    },
    "hero_btns": {
     "type": "group",
     "settings": {
      "content_direction": "row",
      "vertical_on_mobile": false,
      "horizontal_alignment": "center",
      "gap": 12,
      "width": "fit-content",
      "width_mobile": "fit-content"
     },
     "blocks": {
      "hero_b1": {
       "type": "button",
       "settings": {
        "label": "Damen",
        "link": "shopify://collections/women",
        "style_class": "button"
       }
      },
      "hero_b2": {
       "type": "button",
       "settings": {
        "label": "Herren",
        "link": "shopify://collections/men",
        "style_class": "button-secondary"
       }
      }
     },
     "block_order": [
      "hero_b1",
      "hero_b2"
     ]
    }
   },
   "block_order": [
    "hero_t1",
    "hero_t2",
    "hero_btns"
   ],
   "settings": {
    "media_type_1": "image",
    "image_1": "shopify://shop_images/Daily_Berlin_Banner1.png",
    "horizontal_alignment_flex_direction_column": "center",
    "vertical_alignment_flex_direction_column": "center",
    "gap": 16,
    "section_width": "full-width",
    "section_height": "large",
    "color_scheme": "scheme-6",
    "toggle_overlay": true,
    "overlay_color": "#00000040",
    "overlay_style": "solid",
    "padding-block-start": 48,
    "padding-block-end": 48
   },
   "name": "Hero"
  },
  "trust_db": {
   "type": "section",
   "blocks": {
    "feat_0": {
     "type": "group",
     "settings": {
      "content_direction": "column",
      "horizontal_alignment_flex_direction_column": "center",
      "gap": 8,
      "width": "fill",
      "width_mobile": "fill",
      "padding-block-start": 16,
      "padding-block-end": 16,
      "padding-inline-start": 12,
      "padding-inline-end": 12
     },
     "blocks": {
      "feat_0_icon": {
       "type": "icon",
       "settings": {
        "icon": "truck",
        "width": 32
       }
      },
      "feat_0_title": {
       "type": "text",
       "settings": {
        "text": "<p><strong>Kostenloser Versand</strong></p>",
        "type_preset": "h5",
        "alignment": "center",
        "width": "100%"
       }
      },
      "feat_0_text": {
       "type": "text",
       "settings": {
        "text": "<p>Kostenloser Versand in ganz Deutschland, Österreich, Frankreich und Liechtenstein</p>",
        "type_preset": "rte",
        "alignment": "center",
        "width": "100%"
       }
      }
     },
     "block_order": [
      "feat_0_icon",
      "feat_0_title",
      "feat_0_text"
     ]
    },
    "feat_1": {
     "type": "group",
     "settings": {
      "content_direction": "column",
      "horizontal_alignment_flex_direction_column": "center",
      "gap": 8,
      "width": "fill",
      "width_mobile": "fill",
      "padding-block-start": 16,
      "padding-block-end": 16,
      "padding-inline-start": 12,
      "padding-inline-end": 12
     },
     "blocks": {
      "feat_1_icon": {
       "type": "icon",
       "settings": {
        "icon": "return",
        "width": 32
       }
      },
      "feat_1_title": {
       "type": "text",
       "settings": {
        "text": "<p><strong>60-Tage-Rückgabegarantie</strong></p>",
        "type_preset": "h5",
        "alignment": "center",
        "width": "100%"
       }
      },
      "feat_1_text": {
       "type": "text",
       "settings": {
        "text": "<p>Nicht zufrieden mit Ihrem Kauf? Senden Sie ihn innerhalb von 60 Tagen zurück.</p>",
        "type_preset": "rte",
        "alignment": "center",
        "width": "100%"
       }
      }
     },
     "block_order": [
      "feat_1_icon",
      "feat_1_title",
      "feat_1_text"
     ]
    },
    "feat_2": {
     "type": "group",
     "settings": {
      "content_direction": "column",
      "horizontal_alignment_flex_direction_column": "center",
      "gap": 8,
      "width": "fill",
      "width_mobile": "fill",
      "padding-block-start": 16,
      "padding-block-end": 16,
      "padding-inline-start": 12,
      "padding-inline-end": 12
     },
     "blocks": {
      "feat_2_icon": {
       "type": "icon",
       "settings": {
        "icon": "chat_bubble",
        "width": 32
       }
      },
      "feat_2_title": {
       "type": "text",
       "settings": {
        "text": "<p><strong>24/7 Kundenservice</strong></p>",
        "type_preset": "h5",
        "alignment": "center",
        "width": "100%"
       }
      },
      "feat_2_text": {
       "type": "text",
       "settings": {
        "text": "<p>Wir sind jederzeit für Sie da, Tag und Nacht. Kontaktieren Sie uns jederzeit!</p>",
        "type_preset": "rte",
        "alignment": "center",
        "width": "100%"
       }
      }
     },
     "block_order": [
      "feat_2_icon",
      "feat_2_title",
      "feat_2_text"
     ]
    }
   },
   "block_order": [
    "feat_0",
    "feat_1",
    "feat_2"
   ],
   "settings": {
    "content_direction": "row",
    "vertical_on_mobile": true,
    "gap": 16,
    "section_width": "page-width",
    "color_scheme": "scheme-1",
    "padding-block-start": 40,
    "padding-block-end": 40
   },
   "name": "Vorteile"
  },
  "collections_db": {
   "type": "collection-list",
   "name": "Kollektionen",
   "settings": {
    "collection_list": [
     "women",
     "men"
    ],
    "layout_type": "grid",
    "columns": 2,
    "mobile_columns": "1",
    "section_width": "page-width",
    "padding-block-start": 24,
    "padding-block-end": 24
   },
   "blocks": {
    "coll_head": {
     "type": "text",
     "settings": {
      "text": "<h2>Kollektionen</h2>",
      "type_preset": "h3",
      "alignment": "center",
      "width": "100%"
     }
    },
    "static-collection-card": {
     "type": "_collection-card",
     "static": true,
     "settings": {
      "horizontal_alignment": "center",
      "vertical_alignment": "center",
      "placement": "on_image"
     },
     "blocks": {
      "collection-card-image": {
       "type": "_collection-card-image",
       "static": true,
       "settings": {
        "image_ratio": "square"
       }
      },
      "collection-title": {
       "type": "collection-title",
       "settings": {
        "type_preset": "h3",
        "alignment": "center",
        "background": true,
        "background_color": "#ffffff",
        "padding-block-start": 8,
        "padding-block-end": 8,
        "padding-inline-start": 16,
        "padding-inline-end": 16
       }
      }
     },
     "block_order": [
      "collection-title"
     ]
    }
   },
   "block_order": [
    "coll_head"
   ]
  },
  "about_db": {
   "type": "media-with-content",
   "settings": {
    "media_position": "right",
    "media_width": "medium",
    "media_height": "auto",
    "color_scheme": "scheme-1"
   },
   "blocks": {
    "media": {
     "type": "_media-without-appearance",
     "static": true,
     "settings": {
      "image": "shopify://shop_images/Daily_Berlin_About_us.png",
      "media_type": "image"
     }
    },
    "content": {
     "type": "_content-without-appearance",
     "static": true,
     "settings": {
      "horizontal_alignment_flex_direction_column": "flex-start",
      "vertical_alignment_flex_direction_column": "center",
      "gap": 20,
      "padding-block-start": 48,
      "padding-block-end": 48,
      "padding-inline-start": 48,
      "padding-inline-end": 48
     },
     "blocks": {
      "about_h": {
       "type": "text",
       "settings": {
        "text": "<h2>Über uns</h2>",
        "type_preset": "h3",
        "alignment": "left",
        "width": "100%"
       }
      },
      "about_t": {
       "type": "text",
       "settings": {
        "text": "<p>Daily Berlin entstand aus der Liebe zu Stil, Street Culture und durchdachtem Design.<br/><br/>Wir glauben, dass Kleidung mehr ist als nur das, was man trägt. Sie zeigt, wie man in der Welt auftritt.<br/><br/>Unsere Kollektionen verbinden moderne Ästhetik mit alltäglichem Komfort – mit Sorgfalt gefertigt für Qualität, Menschen und unseren Planeten.<br/><br/>Zeitlose Pieces, bewusste Entscheidungen, gemacht, um sich mit dir zu bewegen.<br/><br/>Street Vibes. Klares Design. Gemacht, um zu bleiben.<br/><br/>Das ist Daily Berlin.<br/><br/></p>",
        "type_preset": "rte",
        "alignment": "left",
        "width": "100%"
       }
      },
      "about_b": {
       "type": "button",
       "settings": {
        "label": "Mehr über uns",
        "link": "shopify://pages/uber-uns",
        "style_class": "button"
       }
      }
     },
     "block_order": [
      "about_h",
      "about_t",
      "about_b"
     ]
    }
   },
   "name": "Über uns"
  },
  "faq_db": {
   "type": "section",
   "blocks": {
    "faq_title": {
     "type": "text",
     "settings": {
      "text": "<h2>Häufig gestellte Fragen</h2>",
      "type_preset": "h3",
      "alignment": "center",
      "width": "100%"
     }
    },
    "faq_acc": {
     "type": "accordion",
     "settings": {
      "icon": "plus",
      "dividers": true,
      "type_preset": "h6"
     },
     "blocks": {
      "faq_row_1": {
       "type": "_accordion-row",
       "settings": {
        "heading": "Wie lauten Ihre Rückgabebedingungen?"
       },
       "blocks": {
        "faq_ans_1": {
         "type": "text",
         "settings": {
          "text": "<p>Wir gewähren ein 60-tägiges Rückgaberecht für alle ungetragenen Artikel, an denen die Originaletiketten noch angebracht sind. Die Artikel müssen sich im Originalzustand befinden, damit eine vollständige Rückerstattung gewährt werden kann.</p>",
          "type_preset": "rte",
          "alignment": "left",
          "width": "100%"
         }
        }
       },
       "block_order": [
        "faq_ans_1"
       ]
      },
      "faq_row_2": {
       "type": "_accordion-row",
       "settings": {
        "heading": "Wie lange dauert der Versand?"
       },
       "blocks": {
        "faq_ans_2": {
         "type": "text",
         "settings": {
          "text": "<p>Bearbeitungszeit: 1–2 Werktage</p><p> Voraussichtliche Versanddauer: 3–7 Werktage</p><p>In den meisten Fällen trifft Ihre Bestellung innerhalb von insgesamt 4–9 Werktagen ein.<br/><br/></p>",
          "type_preset": "rte",
          "alignment": "left",
          "width": "100%"
         }
        }
       },
       "block_order": [
        "faq_ans_2"
       ]
      },
      "faq_row_3": {
       "type": "_accordion-row",
       "settings": {
        "heading": "Bieten Sie internationalen Versand an?"
       },
       "blocks": {
        "faq_ans_3": {
         "type": "text",
         "settings": {
          "text": "<p>Derzeit liefern wir nur innerhalb Deutschlands, Österreichs, Frankreich und Liechtensteins.</p>",
          "type_preset": "rte",
          "alignment": "left",
          "width": "100%"
         }
        }
       },
       "block_order": [
        "faq_ans_3"
       ]
      },
      "faq_row_4": {
       "type": "_accordion-row",
       "settings": {
        "heading": "Wie pflege ich meine Kleidungsstücke?"
       },
       "blocks": {
        "faq_ans_4": {
         "type": "text",
         "settings": {
          "text": "<p>Die Pflegehinweise finden Sie auf dem Etikett jedes Kleidungsstücks. Generell empfehlen wir, die Kleidungsstücke in kaltem Wasser zu waschen und zum Trocknen aufzuhängen, um die Qualität und Langlebigkeit Ihrer Kleidungsstücke zu erhalten.</p>",
          "type_preset": "rte",
          "alignment": "left",
          "width": "100%"
         }
        }
       },
       "block_order": [
        "faq_ans_4"
       ]
      }
     },
     "block_order": [
      "faq_row_1",
      "faq_row_2",
      "faq_row_3",
      "faq_row_4"
     ]
    }
   },
   "block_order": [
    "faq_title",
    "faq_acc"
   ],
   "settings": {
    "content_direction": "column",
    "horizontal_alignment_flex_direction_column": "center",
    "gap": 24,
    "section_width": "page-width",
    "color_scheme": "scheme-1",
    "padding-block-start": 48,
    "padding-block-end": 48
   },
   "name": "FAQ"
  }
 },
 "order": [
  "hero_db",
  "trust_db",
  "collections_db",
  "about_db",
  "faq_db"
 ]
}
DBEOF
cat > sections/header-group.json <<'DBEOF'
{
 "type": "header",
 "name": "Header",
 "sections": {
  "header_announcements_9jGBFp": {
   "type": "header-announcements",
   "name": "t:names.announcement_bar",
   "blocks": {
    "announcement_BxgCk9": {
     "type": "_announcement",
     "settings": {
      "text": "Kostenloser Versand in ganz Deutschland, Österreich, Frankreich und Liechtenstein",
      "link": "",
      "font_size": "0.875rem",
      "case": "none"
     }
    }
   },
   "block_order": [
    "announcement_BxgCk9"
   ],
   "settings": {
    "speed": 5,
    "section_width": "page-width",
    "color_scheme": "scheme-5",
    "divider_width": 0,
    "padding-block-start": 10,
    "padding-block-end": 10
   }
  },
  "header_section": {
   "type": "header",
   "blocks": {
    "header-logo": {
     "type": "_header-logo",
     "static": true,
     "settings": {
      "hide_logo_on_home_page": false
     }
    },
    "header-menu": {
     "type": "_header-menu",
     "static": true,
     "settings": {
      "menu": "main-menu-1",
      "type_font_primary_size": "0.875rem",
      "menu_font_style": "inverse",
      "type_font_primary_link": "body",
      "type_case_primary_link": "uppercase",
      "menu_style": "featured_products",
      "image_border_radius": 0,
      "navigation_bar": false,
      "drawer_accordion": true,
      "drawer_accordion_expand_first": false,
      "drawer_dividers": true
     }
    }
   },
   "settings": {
    "logo_position": "center",
    "menu_position": "center",
    "menu_row": "bottom",
    "show_search": true,
    "search_position": "left",
    "search_row": "top",
    "show_country": false,
    "show_language": true,
    "localization_font": "body",
    "localization_font_size": "0.875rem",
    "localization_position": "right",
    "localization_row": "top",
    "section_width": "page-width",
    "section_height": "standard",
    "enable_sticky_header": "always",
    "divider_width": 1,
    "divider_size": "page-width",
    "border_width": 0,
    "color_scheme_top": "scheme-1",
    "color_scheme_bottom": "scheme-1",
    "color_scheme_transparent": "scheme-6",
    "enable_transparent_header_home": false,
    "enable_transparent_header_product": false,
    "enable_transparent_header_collection": false
   }
  }
 },
 "order": [
  "header_announcements_9jGBFp",
  "header_section"
 ]
}
DBEOF
cat > sections/footer-group.json <<'DBEOF'
{
 "type": "footer",
 "name": "Footer",
 "sections": {
  "footer_m9NzUG": {
   "type": "footer",
   "name": "t:names.footer",
   "blocks": {
    "ft_info": {
     "type": "group",
     "settings": {
      "content_direction": "column",
      "horizontal_alignment_flex_direction_column": "flex-start",
      "vertical_alignment_flex_direction_column": "flex-start",
      "gap": 12,
      "width": "fill",
      "width_mobile": "fill"
     },
     "blocks": {
      "ft_info_h": {
       "type": "text",
       "settings": {
        "text": "<h3>Unsere Informationen</h3>",
        "type_preset": "h6",
        "alignment": "left",
        "width": "100%"
       }
      },
      "ft_info_t": {
       "type": "text",
       "settings": {
        "text": "<p><strong>Firmenname: </strong>Daily Berlin<strong><br/></strong><br/><strong>Firmenadresse: </strong>Rosa Luxemburgstraat 11, 1103 DR Amsterdam, Niederlande<br/><br/><strong>Lageradresse: </strong>Jänickestraße 40, 14167 Berlin (Steglitz-Zehlendorf), Deutschland<br/><br/><strong>Firmennummer: </strong>61429573861</p><p><strong>E-Mail:</strong>&nbsp;<a href=\"mailto:support@dailyberlin.de\">support@dailyberlin.de<br/><br/></a><strong>Kundenservice-Zeiten</strong><br/>Montag bis Freitag: 08:00 – 17:00 Uhr<br/>Samstag bis Sonntag: 09:00 – 16:00 Uhr<br/><br/>Durchschnittliche Antwortzeit: innerhalb von 12 Stunden<br/><br/><a href=\"https://www.instagram.com/dailyberlin2026/\" title=\"https://www.instagram.com/dailyberlin2026/\">Instagram Daily Berlin</a></p>",
        "type_preset": "rte",
        "alignment": "left",
        "width": "100%"
       }
      }
     },
     "block_order": [
      "ft_info_h",
      "ft_info_t"
     ]
    },
    "ft_menu1": {
     "type": "menu",
     "settings": {
      "menu": "main-menu-1",
      "heading": "Informationen",
      "heading_preset": "h6",
      "link_preset": "paragraph",
      "menu_spacing": 8
     }
    },
    "ft_menu2": {
     "type": "menu",
     "settings": {
      "menu": "footer",
      "heading": "Rechtliche Hinweise",
      "heading_preset": "h6",
      "link_preset": "paragraph",
      "menu_spacing": 8
     }
    },
    "ft_news": {
     "type": "group",
     "settings": {
      "content_direction": "column",
      "horizontal_alignment_flex_direction_column": "flex-start",
      "vertical_alignment_flex_direction_column": "flex-start",
      "gap": 12,
      "width": "fill",
      "width_mobile": "fill"
     },
     "blocks": {
      "ft_news_h": {
       "type": "text",
       "settings": {
        "text": "<h3>Jetzt anmelden und sparen</h3>",
        "type_preset": "h6",
        "alignment": "left",
        "width": "100%"
       }
      },
      "ft_news_t": {
       "type": "text",
       "settings": {
        "text": "<p>Abonnieren Sie unseren Newsletter und erhalten Sie exklusive Angebote, kostenlose Geschenke und einmalige Deals</p>",
        "type_preset": "rte",
        "alignment": "left",
        "width": "100%"
       }
      },
      "ft_news_f": {
       "type": "email-signup",
       "settings": {
        "width": "fill",
        "inherit_color_scheme": true,
        "border_style": "all",
        "border_width": 1,
        "border_radius": 0,
        "display_type": "arrow",
        "label": "Anmelden",
        "integrated_button": true
       }
      }
     },
     "block_order": [
      "ft_news_h",
      "ft_news_t",
      "ft_news_f"
     ]
    }
   },
   "block_order": [
    "ft_info",
    "ft_menu1",
    "ft_menu2",
    "ft_news"
   ],
   "settings": {
    "section_width": "page-width",
    "gap": 40,
    "color_scheme": "scheme-5",
    "padding-block-start": 56,
    "padding-block-end": 40
   }
  },
  "footer_utilities_jLGE8U": {
   "type": "footer-utilities",
   "name": "t:names.utilities",
   "blocks": {
    "footer_copyright_jweRK8": {
     "type": "footer-copyright",
     "settings": {
      "show_powered_by": false,
      "font_size": "0.75rem",
      "case": "none"
     }
    },
    "ft_pay": {
     "type": "payment-icons",
     "settings": {
      "horizontal_alignment": "center",
      "gap": 8
     }
    },
    "social_links_Ew63Kq": {
     "type": "social-links",
     "settings": {
      "instagram_url": "https://www.instagram.com/dailyberlin2026/"
     }
    }
   },
   "block_order": [
    "footer_copyright_jweRK8",
    "ft_pay",
    "social_links_Ew63Kq"
   ],
   "settings": {
    "section_width": "page-width",
    "gap": 24,
    "divider_thickness": 1,
    "color_scheme": "scheme-5",
    "padding-block-start": 20,
    "padding-block-end": 32
   }
  }
 },
 "order": [
  "footer_m9NzUG",
  "footer_utilities_jLGE8U"
 ]
}
DBEOF
sed '/^\/\*/,/\*\//d' config/settings_data.json > sd.tmp.json
jq '.current.logo="shopify://shop_images/Black_and_White_Minimalist_Elegant_Modern_Typography_Creative_Studio_Brand_Logo_500_x_250_px_500_x_125_px_300_x_100_px_200_x_50_px_300_x_100_px_72_x_18_in_500_x_200_px.png"
 | .current.logo_inverse="shopify://shop_images/Black_and_White_Minimalist_Elegant_Modern_Typography_Creative_Studio_Brand_Logo_500_x_250_px_500_x_125_px_300_x_100_px_200_x_50_px_300_x_100_px_72_x_18_in_500_x_200_px_1.png"
 | .current.favicon="shopify://shop_images/Black_and_White_Minimalist_Elegant_Modern_Typography_Creative_Studio_Brand_Logo_500_x_250_px_3.svg"
 | .current.logo_height=44 | .current.logo_height_mobile=32
 | .current.type_body_font="alegreya_sans_n4" | .current.type_subheading_font="alegreya_sans_n5" | .current.type_heading_font="alegreya_sans_n7" | .current.type_accent_font="alegreya_sans_n7"
 | .current.type_size_paragraph="16"
 | .current.type_case_h1="uppercase" | .current.type_case_h2="uppercase" | .current.type_case_h3="uppercase" | .current.type_case_h4="uppercase"
 | .current.page_width="wide"
 | .current.button_border_radius_primary=0 | .current.button_border_radius_secondary=0 | .current.inputs_border_radius=0 | .current.variant_button_radius=0 | .current.card_corner_radius=0 | .current.badge_corner_radius=0 | .current.popover_border_radius=0
 | .current.badge_sale_color_scheme="scheme-5"
 | .current.color_schemes["scheme-5"].settings.background="#0f0f0f"
 | .current.color_schemes["scheme-5"].settings.foreground_heading="#ffffff"
 | .current.color_schemes["scheme-1"].settings.foreground="#000000"' sd.tmp.json > config/settings_data.json
jq empty config/settings_data.json templates/index.json sections/header-group.json sections/footer-group.json && echo JSONOK
rm sd.tmp.json
