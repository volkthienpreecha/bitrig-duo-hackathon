// Fold & Fetch: resume the blocked Figma UI composition.
// Run via Figma use_figma with figma-use,figma-generate-design,figma-generate-library.
// Target file: 5RQpJ3a4FGxOEzKya5mAeI. Does not modify any game source.
// Loaded guidance and foundation IDs are recorded in ui-figma-status.json.
const spec = {
  "colors": {
    "cream": "#F3E7CF",
    "ink": "#243A40",
    "night": "#17292F",
    "deepTeal": "#245E5A",
    "teal": "#4D9B91",
    "copper": "#B77950",
    "cyan": "#82D9CE",
    "peach": "#F0B49A",
    "gold": "#D7A35C",
    "leaf": "#738A64",
    "muted": "#526368",
    "line": "#CDBF9E"
  },
  "iconPaths": {
    "swipe-left": "M19 12H5 M10 7L5 12L10 17",
    "swipe-right": "M5 12H19 M14 7L19 12L14 17",
    "swipe-up": "M12 19V5 M7 10L12 5L17 10",
    "swipe-down": "M12 5V19 M7 14L12 19L17 14",
    "pause": "M8 5V19 M16 5V19",
    "resume": "M8 5L19 12L8 19Z",
    "restart": "M5 8A8 8 0 1 1 4 15 M5 3V8H10",
    "replay": "M5 8A8 8 0 1 1 4 15 M5 3V8H10",
    "audio-on": "M4 9H8L13 5V19L8 15H4Z M17 8C20 10 20 14 17 16",
    "audio-off": "M4 9H8L13 5V19L8 15H4Z M17 9L22 15 M22 9L17 15",
    "release": "M12 3V13 M8 9L12 13L16 9 M4 17H20V21H4Z",
    "fold": "M3 6L10 3L14 7L21 4V18L14 21L10 17L3 20Z M10 3V17 M14 7V21",
    "bell": "M5 16H19L17 13V9C17 2 7 2 7 9V13Z M10 20H14",
    "check": "M5 12L10 17L19 7"
  },
  "states": {
    "gameplay": {
      "w": 1080,
      "h": 720,
      "scene": [
        {
          "type": "rect",
          "name": "Schematic night",
          "x": 0,
          "y": 0,
          "w": 1080,
          "h": 720,
          "color": "night",
          "radius": 0,
          "opacity": 1
        },
        {
          "type": "rect",
          "name": "Distant rooftop 0",
          "x": 10,
          "y": 236,
          "w": 105,
          "h": 320,
          "color": "ink",
          "radius": 14,
          "opacity": 1
        },
        {
          "type": "rect",
          "name": "Distant rooftop 1",
          "x": 122,
          "y": 306,
          "w": 64,
          "h": 270,
          "color": "ink",
          "radius": 14,
          "opacity": 1
        },
        {
          "type": "rect",
          "name": "Distant rooftop 2",
          "x": 194,
          "y": 208,
          "w": 100,
          "h": 365,
          "color": "ink",
          "radius": 14,
          "opacity": 1
        },
        {
          "type": "rect",
          "name": "Distant rooftop 3",
          "x": 828,
          "y": 272,
          "w": 95,
          "h": 316,
          "color": "ink",
          "radius": 14,
          "opacity": 1
        },
        {
          "type": "rect",
          "name": "Distant rooftop 4",
          "x": 943,
          "y": 224,
          "w": 127,
          "h": 372,
          "color": "ink",
          "radius": 14,
          "opacity": 1
        },
        {
          "type": "rect",
          "name": "Left roof",
          "x": 186,
          "y": 434,
          "w": 300,
          "h": 100,
          "color": "deepTeal",
          "radius": 22,
          "opacity": 1
        },
        {
          "type": "rect",
          "name": "Roof cream rim",
          "x": 176,
          "y": 412,
          "w": 324,
          "h": 36,
          "color": "cream",
          "radius": 16,
          "opacity": 1
        },
        {
          "type": "rect",
          "name": "Right roof",
          "x": 666,
          "y": 426,
          "w": 254,
          "h": 108,
          "color": "deepTeal",
          "radius": 22,
          "opacity": 1
        },
        {
          "type": "rect",
          "name": "Right roof cream rim",
          "x": 656,
          "y": 404,
          "w": 274,
          "h": 36,
          "color": "cream",
          "radius": 16,
          "opacity": 1
        },
        {
          "type": "rect",
          "name": "Workshop",
          "x": 210,
          "y": 260,
          "w": 192,
          "h": 155,
          "color": "teal",
          "radius": 25,
          "opacity": 1
        },
        {
          "type": "rect",
          "name": "Workshop warm window",
          "x": 240,
          "y": 297,
          "w": 66,
          "h": 75,
          "color": "peach",
          "radius": 14,
          "opacity": 1
        },
        {
          "type": "rect",
          "name": "Workshop door",
          "x": 321,
          "y": 298,
          "w": 49,
          "h": 117,
          "color": "deepTeal",
          "radius": 10,
          "opacity": 1
        },
        {
          "type": "rect",
          "name": "Copper chute rail",
          "x": 432,
          "y": 215,
          "w": 202,
          "h": 18,
          "color": "copper",
          "radius": 9,
          "opacity": 1
        },
        {
          "type": "rect",
          "name": "Beam ready",
          "x": 484,
          "y": 270,
          "w": 158,
          "h": 28,
          "color": "cream",
          "radius": 10,
          "opacity": 1
        },
        {
          "type": "rect",
          "name": "Soft left planter",
          "x": 192,
          "y": 381,
          "w": 28,
          "h": 33,
          "color": "copper",
          "radius": 7,
          "opacity": 1
        },
        {
          "type": "rect",
          "name": "Soft right planter",
          "x": 865,
          "y": 374,
          "w": 30,
          "h": 30,
          "color": "copper",
          "radius": 7,
          "opacity": 1
        },
        {
          "type": "icon",
          "name": "bell",
          "x": 812,
          "y": 340,
          "w": 40,
          "h": 40,
          "color": "gold",
          "svg": "<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"40\" height=\"40\" viewBox=\"0 0 24 24\" fill=\"none\"><title>bell</title><path d=\"M5 16H19L17 13V9C17 2 7 2 7 9V13Z M10 20H14\" stroke=\"#D7A35C\" stroke-width=\"1.8\" stroke-linecap=\"round\" stroke-linejoin=\"round\"/></svg>"
        },
        {
          "type": "ellipse",
          "name": "Kaprao body marker",
          "x": 352,
          "y": 371,
          "w": 65,
          "h": 39,
          "color": "gold"
        },
        {
          "type": "ellipse",
          "name": "Kaprao head marker",
          "x": 390,
          "y": 359,
          "w": 34,
          "h": 33,
          "color": "gold"
        },
        {
          "type": "rect",
          "name": "Kaprao scarf marker",
          "x": 392,
          "y": 388,
          "w": 23,
          "h": 8,
          "color": "teal",
          "radius": 4,
          "opacity": 1
        },
        {
          "type": "text",
          "name": "Reference label",
          "x": 408,
          "y": 566,
          "text": "Schematic scene for UI placement",
          "size": 12,
          "color": "cream",
          "weight": 400
        }
      ],
      "overlay": [
        {
          "type": "group",
          "name": "Level header",
          "x": 36,
          "y": 32,
          "w": 232,
          "h": 74,
          "children": [
            {
              "type": "text",
              "name": "Game name",
              "x": 16,
              "y": 16,
              "text": "FOLD & FETCH",
              "size": 12,
              "color": "cream",
              "weight": 600
            },
            {
              "type": "text",
              "name": "Level name",
              "x": 16,
              "y": 35,
              "text": "Rooftop repair",
              "size": 18,
              "color": "cream",
              "weight": 600
            }
          ],
          "fill": "night",
          "radius": 16,
          "gap": 4,
          "axis": "VERTICAL",
          "padding": 16
        },
        {
          "type": "group",
          "name": "audio-on control",
          "x": 948,
          "y": 32,
          "w": 44,
          "h": 44,
          "children": [
            {
              "type": "icon",
              "name": "audio-on",
              "x": 10,
              "y": 10,
              "w": 24,
              "h": 24,
              "color": "ink",
              "svg": "<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"24\" height=\"24\" viewBox=\"0 0 24 24\" fill=\"none\"><title>audio on</title><path d=\"M4 9H8L13 5V19L8 15H4Z M17 8C20 10 20 14 17 16\" stroke=\"#243A40\" stroke-width=\"1.8\" stroke-linecap=\"round\" stroke-linejoin=\"round\"/></svg>"
            }
          ],
          "fill": "cream",
          "radius": 16,
          "gap": 0,
          "axis": "HORIZONTAL",
          "padding": 10
        },
        {
          "type": "group",
          "name": "pause control",
          "x": 1000,
          "y": 32,
          "w": 44,
          "h": 44,
          "children": [
            {
              "type": "icon",
              "name": "pause",
              "x": 10,
              "y": 10,
              "w": 24,
              "h": 24,
              "color": "ink",
              "svg": "<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"24\" height=\"24\" viewBox=\"0 0 24 24\" fill=\"none\"><title>pause</title><path d=\"M8 5V19 M16 5V19\" stroke=\"#243A40\" stroke-width=\"1.8\" stroke-linecap=\"round\" stroke-linejoin=\"round\"/></svg>"
            }
          ],
          "fill": "cream",
          "radius": 16,
          "gap": 0,
          "axis": "HORIZONTAL",
          "padding": 10
        },
        {
          "type": "group",
          "name": "Context hint",
          "x": 36,
          "y": 612,
          "w": 446,
          "h": 60,
          "children": [
            {
              "type": "icon",
              "name": "fold",
              "x": 16,
              "y": 18,
              "w": 24,
              "h": 24,
              "color": "ink",
              "svg": "<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"24\" height=\"24\" viewBox=\"0 0 24 24\" fill=\"none\"><title>fold</title><path d=\"M3 6L10 3L14 7L21 4V18L14 21L10 17L3 20Z M10 3V17 M14 7V21\" stroke=\"#243A40\" stroke-width=\"1.8\" stroke-linecap=\"round\" stroke-linejoin=\"round\"/></svg>"
            },
            {
              "type": "group",
              "name": "Hint copy",
              "x": 52,
              "y": 10,
              "w": 368,
              "h": 40,
              "children": [
                {
                  "type": "text",
                  "name": "Hint title",
                  "x": 0,
                  "y": 0,
                  "text": "Fold to aim the chute.",
                  "size": 16,
                  "color": "ink",
                  "weight": 600
                },
                {
                  "type": "text",
                  "name": "Hint detail",
                  "x": 0,
                  "y": 22,
                  "text": "Tap Release when the beam lines up.",
                  "size": 14,
                  "color": "muted",
                  "weight": 400
                }
              ],
              "fill": null,
              "radius": 0,
              "gap": 2,
              "axis": "VERTICAL",
              "padding": 0
            }
          ],
          "fill": "cream",
          "radius": 16,
          "gap": 12,
          "axis": "HORIZONTAL",
          "padding": 16
        },
        {
          "type": "group",
          "name": "Release action",
          "x": 900,
          "y": 620,
          "w": 144,
          "h": 52,
          "children": [
            {
              "type": "icon",
              "name": "release",
              "x": 26.879999999999995,
              "y": 15,
              "w": 22,
              "h": 22,
              "color": "cream",
              "svg": "<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"22\" height=\"22\" viewBox=\"0 0 24 24\" fill=\"none\"><title>release</title><path d=\"M12 3V13 M8 9L12 13L16 9 M4 17H20V21H4Z\" stroke=\"#F3E7CF\" stroke-width=\"1.8\" stroke-linecap=\"round\" stroke-linejoin=\"round\"/></svg>"
            },
            {
              "type": "text",
              "name": "Label",
              "x": 58.879999999999995,
              "y": 16,
              "text": "Release",
              "size": 16,
              "color": "cream",
              "weight": 600
            }
          ],
          "fill": "deepTeal",
          "radius": 16,
          "gap": 10,
          "axis": "HORIZONTAL",
          "padding": 16
        }
      ]
    },
    "pause": {
      "w": 1080,
      "h": 720,
      "scene": [
        {
          "type": "rect",
          "name": "Schematic night",
          "x": 0,
          "y": 0,
          "w": 1080,
          "h": 720,
          "color": "night",
          "radius": 0,
          "opacity": 1
        },
        {
          "type": "rect",
          "name": "Distant rooftop 0",
          "x": 10,
          "y": 236,
          "w": 105,
          "h": 320,
          "color": "ink",
          "radius": 14,
          "opacity": 1
        },
        {
          "type": "rect",
          "name": "Distant rooftop 1",
          "x": 122,
          "y": 306,
          "w": 64,
          "h": 270,
          "color": "ink",
          "radius": 14,
          "opacity": 1
        },
        {
          "type": "rect",
          "name": "Distant rooftop 2",
          "x": 194,
          "y": 208,
          "w": 100,
          "h": 365,
          "color": "ink",
          "radius": 14,
          "opacity": 1
        },
        {
          "type": "rect",
          "name": "Distant rooftop 3",
          "x": 828,
          "y": 272,
          "w": 95,
          "h": 316,
          "color": "ink",
          "radius": 14,
          "opacity": 1
        },
        {
          "type": "rect",
          "name": "Distant rooftop 4",
          "x": 943,
          "y": 224,
          "w": 127,
          "h": 372,
          "color": "ink",
          "radius": 14,
          "opacity": 1
        },
        {
          "type": "rect",
          "name": "Left roof",
          "x": 186,
          "y": 434,
          "w": 300,
          "h": 100,
          "color": "deepTeal",
          "radius": 22,
          "opacity": 1
        },
        {
          "type": "rect",
          "name": "Roof cream rim",
          "x": 176,
          "y": 412,
          "w": 324,
          "h": 36,
          "color": "cream",
          "radius": 16,
          "opacity": 1
        },
        {
          "type": "rect",
          "name": "Right roof",
          "x": 666,
          "y": 426,
          "w": 254,
          "h": 108,
          "color": "deepTeal",
          "radius": 22,
          "opacity": 1
        },
        {
          "type": "rect",
          "name": "Right roof cream rim",
          "x": 656,
          "y": 404,
          "w": 274,
          "h": 36,
          "color": "cream",
          "radius": 16,
          "opacity": 1
        },
        {
          "type": "rect",
          "name": "Workshop",
          "x": 210,
          "y": 260,
          "w": 192,
          "h": 155,
          "color": "teal",
          "radius": 25,
          "opacity": 1
        },
        {
          "type": "rect",
          "name": "Workshop warm window",
          "x": 240,
          "y": 297,
          "w": 66,
          "h": 75,
          "color": "peach",
          "radius": 14,
          "opacity": 1
        },
        {
          "type": "rect",
          "name": "Workshop door",
          "x": 321,
          "y": 298,
          "w": 49,
          "h": 117,
          "color": "deepTeal",
          "radius": 10,
          "opacity": 1
        },
        {
          "type": "rect",
          "name": "Copper chute rail",
          "x": 432,
          "y": 215,
          "w": 202,
          "h": 18,
          "color": "copper",
          "radius": 9,
          "opacity": 1
        },
        {
          "type": "rect",
          "name": "Beam ready",
          "x": 484,
          "y": 270,
          "w": 158,
          "h": 28,
          "color": "cream",
          "radius": 10,
          "opacity": 1
        },
        {
          "type": "rect",
          "name": "Soft left planter",
          "x": 192,
          "y": 381,
          "w": 28,
          "h": 33,
          "color": "copper",
          "radius": 7,
          "opacity": 1
        },
        {
          "type": "rect",
          "name": "Soft right planter",
          "x": 865,
          "y": 374,
          "w": 30,
          "h": 30,
          "color": "copper",
          "radius": 7,
          "opacity": 1
        },
        {
          "type": "icon",
          "name": "bell",
          "x": 812,
          "y": 340,
          "w": 40,
          "h": 40,
          "color": "gold",
          "svg": "<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"40\" height=\"40\" viewBox=\"0 0 24 24\" fill=\"none\"><title>bell</title><path d=\"M5 16H19L17 13V9C17 2 7 2 7 9V13Z M10 20H14\" stroke=\"#D7A35C\" stroke-width=\"1.8\" stroke-linecap=\"round\" stroke-linejoin=\"round\"/></svg>"
        },
        {
          "type": "ellipse",
          "name": "Kaprao body marker",
          "x": 352,
          "y": 371,
          "w": 65,
          "h": 39,
          "color": "gold"
        },
        {
          "type": "ellipse",
          "name": "Kaprao head marker",
          "x": 390,
          "y": 359,
          "w": 34,
          "h": 33,
          "color": "gold"
        },
        {
          "type": "rect",
          "name": "Kaprao scarf marker",
          "x": 392,
          "y": 388,
          "w": 23,
          "h": 8,
          "color": "teal",
          "radius": 4,
          "opacity": 1
        },
        {
          "type": "text",
          "name": "Reference label",
          "x": 408,
          "y": 566,
          "text": "Schematic scene for UI placement",
          "size": 12,
          "color": "cream",
          "weight": 400
        }
      ],
      "overlay": [
        {
          "type": "rect",
          "name": "Pause dim",
          "x": 0,
          "y": 0,
          "w": 1080,
          "h": 720,
          "color": "night",
          "radius": 0,
          "opacity": 0.52
        },
        {
          "type": "group",
          "name": "Pause panel",
          "x": 350,
          "y": 188,
          "w": 380,
          "h": 344,
          "children": [
            {
              "type": "text",
              "name": "Pause title",
              "x": 32,
              "y": 32,
              "text": "Taking a breather",
              "size": 28,
              "color": "ink",
              "weight": 700
            },
            {
              "type": "text",
              "name": "Pause detail",
              "x": 32,
              "y": 85,
              "text": "Kaprao can wait.",
              "size": 14,
              "color": "muted",
              "weight": 400
            },
            {
              "type": "group",
              "name": "Resume action",
              "x": 32,
              "y": 120.5,
              "w": 316,
              "h": 52,
              "children": [
                {
                  "type": "icon",
                  "name": "resume",
                  "x": 117.03999999999999,
                  "y": 15,
                  "w": 22,
                  "h": 22,
                  "color": "cream",
                  "svg": "<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"22\" height=\"22\" viewBox=\"0 0 24 24\" fill=\"none\"><title>resume</title><path d=\"M8 5L19 12L8 19Z\" stroke=\"#F3E7CF\" stroke-width=\"1.8\" stroke-linecap=\"round\" stroke-linejoin=\"round\"/></svg>"
                },
                {
                  "type": "text",
                  "name": "Label",
                  "x": 149.04,
                  "y": 16,
                  "text": "Resume",
                  "size": 16,
                  "color": "cream",
                  "weight": 600
                }
              ],
              "fill": "deepTeal",
              "radius": 16,
              "gap": 10,
              "axis": "HORIZONTAL",
              "padding": 16
            },
            {
              "type": "group",
              "name": "Restart action",
              "x": 32,
              "y": 190.5,
              "w": 316,
              "h": 52,
              "children": [
                {
                  "type": "icon",
                  "name": "restart",
                  "x": 112.88,
                  "y": 15,
                  "w": 22,
                  "h": 22,
                  "color": "ink",
                  "svg": "<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"22\" height=\"22\" viewBox=\"0 0 24 24\" fill=\"none\"><title>restart</title><path d=\"M5 8A8 8 0 1 1 4 15 M5 3V8H10\" stroke=\"#243A40\" stroke-width=\"1.8\" stroke-linecap=\"round\" stroke-linejoin=\"round\"/></svg>"
                },
                {
                  "type": "text",
                  "name": "Label",
                  "x": 144.88,
                  "y": 16,
                  "text": "Restart",
                  "size": 16,
                  "color": "ink",
                  "weight": 600
                }
              ],
              "fill": "cream",
              "radius": 16,
              "gap": 10,
              "axis": "HORIZONTAL",
              "padding": 16
            },
            {
              "type": "group",
              "name": "Audio row",
              "x": 32,
              "y": 260.5,
              "w": 316,
              "h": 44,
              "children": [
                {
                  "type": "icon",
                  "name": "audio-on",
                  "x": 0,
                  "y": 10,
                  "w": 24,
                  "h": 24,
                  "color": "ink",
                  "svg": "<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"24\" height=\"24\" viewBox=\"0 0 24 24\" fill=\"none\"><title>audio on</title><path d=\"M4 9H8L13 5V19L8 15H4Z M17 8C20 10 20 14 17 16\" stroke=\"#243A40\" stroke-width=\"1.8\" stroke-linecap=\"round\" stroke-linejoin=\"round\"/></svg>"
                },
                {
                  "type": "text",
                  "name": "Audio label",
                  "x": 34,
                  "y": 13.25,
                  "text": "Sound on",
                  "size": 14,
                  "color": "ink",
                  "weight": 600
                }
              ],
              "fill": null,
              "radius": 0,
              "gap": 10,
              "axis": "HORIZONTAL",
              "padding": 0
            }
          ],
          "fill": "cream",
          "radius": 28,
          "gap": 18,
          "axis": "VERTICAL",
          "padding": 32
        }
      ]
    },
    "completion": {
      "w": 1080,
      "h": 720,
      "scene": [
        {
          "type": "rect",
          "name": "Schematic night",
          "x": 0,
          "y": 0,
          "w": 1080,
          "h": 720,
          "color": "night",
          "radius": 0,
          "opacity": 1
        },
        {
          "type": "rect",
          "name": "Distant rooftop 0",
          "x": 10,
          "y": 236,
          "w": 105,
          "h": 320,
          "color": "ink",
          "radius": 14,
          "opacity": 1
        },
        {
          "type": "rect",
          "name": "Distant rooftop 1",
          "x": 122,
          "y": 306,
          "w": 64,
          "h": 270,
          "color": "ink",
          "radius": 14,
          "opacity": 1
        },
        {
          "type": "rect",
          "name": "Distant rooftop 2",
          "x": 194,
          "y": 208,
          "w": 100,
          "h": 365,
          "color": "ink",
          "radius": 14,
          "opacity": 1
        },
        {
          "type": "rect",
          "name": "Distant rooftop 3",
          "x": 828,
          "y": 272,
          "w": 95,
          "h": 316,
          "color": "ink",
          "radius": 14,
          "opacity": 1
        },
        {
          "type": "rect",
          "name": "Distant rooftop 4",
          "x": 943,
          "y": 224,
          "w": 127,
          "h": 372,
          "color": "ink",
          "radius": 14,
          "opacity": 1
        },
        {
          "type": "rect",
          "name": "Left roof",
          "x": 186,
          "y": 434,
          "w": 300,
          "h": 100,
          "color": "deepTeal",
          "radius": 22,
          "opacity": 1
        },
        {
          "type": "rect",
          "name": "Roof cream rim",
          "x": 176,
          "y": 412,
          "w": 324,
          "h": 36,
          "color": "cream",
          "radius": 16,
          "opacity": 1
        },
        {
          "type": "rect",
          "name": "Right roof",
          "x": 666,
          "y": 426,
          "w": 254,
          "h": 108,
          "color": "deepTeal",
          "radius": 22,
          "opacity": 1
        },
        {
          "type": "rect",
          "name": "Right roof cream rim",
          "x": 656,
          "y": 404,
          "w": 274,
          "h": 36,
          "color": "cream",
          "radius": 16,
          "opacity": 1
        },
        {
          "type": "rect",
          "name": "Workshop",
          "x": 210,
          "y": 260,
          "w": 192,
          "h": 155,
          "color": "teal",
          "radius": 25,
          "opacity": 1
        },
        {
          "type": "rect",
          "name": "Workshop warm window",
          "x": 240,
          "y": 297,
          "w": 66,
          "h": 75,
          "color": "peach",
          "radius": 14,
          "opacity": 1
        },
        {
          "type": "rect",
          "name": "Workshop door",
          "x": 321,
          "y": 298,
          "w": 49,
          "h": 117,
          "color": "deepTeal",
          "radius": 10,
          "opacity": 1
        },
        {
          "type": "rect",
          "name": "Copper chute rail",
          "x": 432,
          "y": 215,
          "w": 202,
          "h": 18,
          "color": "copper",
          "radius": 9,
          "opacity": 1
        },
        {
          "type": "rect",
          "name": "Beam ready",
          "x": 484,
          "y": 270,
          "w": 158,
          "h": 28,
          "color": "cream",
          "radius": 10,
          "opacity": 1
        },
        {
          "type": "rect",
          "name": "Soft left planter",
          "x": 192,
          "y": 381,
          "w": 28,
          "h": 33,
          "color": "copper",
          "radius": 7,
          "opacity": 1
        },
        {
          "type": "rect",
          "name": "Soft right planter",
          "x": 865,
          "y": 374,
          "w": 30,
          "h": 30,
          "color": "copper",
          "radius": 7,
          "opacity": 1
        },
        {
          "type": "icon",
          "name": "bell",
          "x": 812,
          "y": 340,
          "w": 40,
          "h": 40,
          "color": "gold",
          "svg": "<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"40\" height=\"40\" viewBox=\"0 0 24 24\" fill=\"none\"><title>bell</title><path d=\"M5 16H19L17 13V9C17 2 7 2 7 9V13Z M10 20H14\" stroke=\"#D7A35C\" stroke-width=\"1.8\" stroke-linecap=\"round\" stroke-linejoin=\"round\"/></svg>"
        },
        {
          "type": "ellipse",
          "name": "Kaprao body marker",
          "x": 352,
          "y": 371,
          "w": 65,
          "h": 39,
          "color": "gold"
        },
        {
          "type": "ellipse",
          "name": "Kaprao head marker",
          "x": 390,
          "y": 359,
          "w": 34,
          "h": 33,
          "color": "gold"
        },
        {
          "type": "rect",
          "name": "Kaprao scarf marker",
          "x": 392,
          "y": 388,
          "w": 23,
          "h": 8,
          "color": "teal",
          "radius": 4,
          "opacity": 1
        },
        {
          "type": "text",
          "name": "Reference label",
          "x": 408,
          "y": 566,
          "text": "Schematic scene for UI placement",
          "size": 12,
          "color": "cream",
          "weight": 400
        }
      ],
      "overlay": [
        {
          "type": "rect",
          "name": "Complete dim",
          "x": 0,
          "y": 0,
          "w": 1080,
          "h": 720,
          "color": "night",
          "radius": 0,
          "opacity": 0.42
        },
        {
          "type": "group",
          "name": "Complete panel",
          "x": 350,
          "y": 188,
          "w": 380,
          "h": 344,
          "children": [
            {
              "type": "icon",
              "name": "bell",
              "x": 32,
              "y": 32,
              "w": 40,
              "h": 40,
              "color": "deepTeal",
              "svg": "<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"40\" height=\"40\" viewBox=\"0 0 24 24\" fill=\"none\"><title>bell</title><path d=\"M5 16H19L17 13V9C17 2 7 2 7 9V13Z M10 20H14\" stroke=\"#245E5A\" stroke-width=\"1.8\" stroke-linecap=\"round\" stroke-linejoin=\"round\"/></svg>"
            },
            {
              "type": "text",
              "name": "Complete title",
              "x": 32,
              "y": 90,
              "text": "Bell reached!",
              "size": 28,
              "color": "ink",
              "weight": 700
            },
            {
              "type": "text",
              "name": "Complete detail",
              "x": 32,
              "y": 143,
              "text": "Nice work, Kaprao.",
              "size": 14,
              "color": "muted",
              "weight": 400
            },
            {
              "type": "group",
              "name": "Replay action",
              "x": 32,
              "y": 178.5,
              "w": 316,
              "h": 52,
              "children": [
                {
                  "type": "icon",
                  "name": "replay",
                  "x": 117.03999999999999,
                  "y": 15,
                  "w": 22,
                  "h": 22,
                  "color": "cream",
                  "svg": "<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"22\" height=\"22\" viewBox=\"0 0 24 24\" fill=\"none\"><title>replay</title><path d=\"M5 8A8 8 0 1 1 4 15 M5 3V8H10\" stroke=\"#F3E7CF\" stroke-width=\"1.8\" stroke-linecap=\"round\" stroke-linejoin=\"round\"/></svg>"
                },
                {
                  "type": "text",
                  "name": "Label",
                  "x": 149.04,
                  "y": 16,
                  "text": "Replay",
                  "size": 16,
                  "color": "cream",
                  "weight": 600
                }
              ],
              "fill": "deepTeal",
              "radius": 16,
              "gap": 10,
              "axis": "HORIZONTAL",
              "padding": 16
            },
            {
              "type": "group",
              "name": "Audio row",
              "x": 32,
              "y": 248.5,
              "w": 316,
              "h": 44,
              "children": [
                {
                  "type": "icon",
                  "name": "audio-on",
                  "x": 0,
                  "y": 10,
                  "w": 24,
                  "h": 24,
                  "color": "ink",
                  "svg": "<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"24\" height=\"24\" viewBox=\"0 0 24 24\" fill=\"none\"><title>audio on</title><path d=\"M4 9H8L13 5V19L8 15H4Z M17 8C20 10 20 14 17 16\" stroke=\"#243A40\" stroke-width=\"1.8\" stroke-linecap=\"round\" stroke-linejoin=\"round\"/></svg>"
                },
                {
                  "type": "text",
                  "name": "Audio label",
                  "x": 34,
                  "y": 13.25,
                  "text": "Sound on",
                  "size": 14,
                  "color": "ink",
                  "weight": 600
                }
              ],
              "fill": null,
              "radius": 0,
              "gap": 10,
              "axis": "HORIZONTAL",
              "padding": 0
            }
          ],
          "fill": "cream",
          "radius": 28,
          "gap": 18,
          "axis": "VERTICAL",
          "padding": 32
        }
      ]
    }
  },
  "hints": [
    [
      "swipe-left",
      "Swipe left",
      "Move left"
    ],
    [
      "swipe-right",
      "Swipe right",
      "Move right"
    ],
    [
      "swipe-up",
      "Swipe up",
      "Jump"
    ],
    [
      "swipe-down",
      "Swipe down in the air",
      "Dash"
    ],
    [
      "fold",
      "Fold to aim the chute.",
      "Depth and height change together."
    ],
    [
      "release",
      "Beam lined up?",
      "Tap Release."
    ]
  ],
  "referenceOnly": true
};

await Promise.all(['Regular','SemiBold','Bold'].map(style=>figma.loadFontAsync({family:'Nunito',style})));
const made=[];const vars=Object.fromEntries((await figma.variables.getLocalVariablesAsync()).map(v=>[v.name,v]));
const sem={cream:'surface',ink:'text',night:'canvas',deepTeal:'action',cyan:'accent',line:'border',muted:'muted',gold:'celebration'};
function p(color){let v=vars[sem[color]?'ui/'+sem[color]:'palette/'+color];return figma.variables.setBoundVariableForPaint({type:'SOLID',color:{r:0,g:0,b:0}},'color',v);}
function record(n){made.push(n.id);return n;}
function tx(s,size=16,color='ink',weight='Regular'){let t=record(figma.createText());t.name=s;t.fontName={family:'Nunito',style:weight};t.fontSize=size;t.lineHeight={unit:'PIXELS',value:Math.ceil(size*1.25)};t.textAutoResize='WIDTH_AND_HEIGHT';t.characters=s;t.fills=[p(color)];return t;}
function frame(name,x,y,w,h,color='cream'){const f=record(figma.createFrame());f.name=name;f.x=x;f.y=y;f.resize(w,h);f.fills=color?[p(color)]:[];return f;}
function build(e,parent){let n;
if(e.type==='group'){n=record(e.axis?figma.createAutoLayout(e.axis):figma.createFrame());n.name=e.name;n.resize(e.w,e.h);n.fills=e.fill?[p(e.fill)]:[];n.cornerRadius=e.radius||0;if(e.radius)n.setBoundVariable('cornerRadius',vars[e.radius===28?'radius/panel':'radius/control']);if(e.axis){n.primaryAxisSizingMode='FIXED';n.counterAxisSizingMode='FIXED';n.itemSpacing=e.gap||0;n.counterAxisAlignItems=e.axis==='HORIZONTAL'?'CENTER':'MIN';n.primaryAxisAlignItems=(/action|control/.test(e.name))?'CENTER':'MIN';for(const k of ['paddingLeft','paddingRight','paddingTop','paddingBottom'])n[k]=e.padding||0;if(vars['space/'+e.gap])n.setBoundVariable('itemSpacing',vars['space/'+e.gap]);if(vars['space/'+e.padding])for(const k of ['paddingLeft','paddingRight','paddingTop','paddingBottom'])n.setBoundVariable(k,vars['space/'+e.padding]);}parent.appendChild(n);for(const child of e.children)build(child,n);
}else if(e.type==='text'){n=tx(e.text,e.size,e.color,e.weight>=700?'Bold':e.weight>=600?'SemiBold':'Regular');n.name=e.name;parent.appendChild(n);
}else if(e.type==='icon'){n=record(figma.createNodeFromSvg(e.svg));n.name=e.name;parent.appendChild(n);n.resize(e.w,e.h);for(const v of n.findAll(()=>true)){made.push(v.id);if('strokes' in v && v.strokes.length)v.strokes=[p(e.color)];if('fills' in v && v.fills.length)v.fills=[p(e.color)];}
}else if(e.type==='rect'||e.type==='ellipse'){n=record(e.type==='ellipse'?figma.createEllipse():figma.createRectangle());n.name=e.name;n.resize(e.w,e.h);n.fills=[p(e.color)];if(e.type==='rect')n.cornerRadius=e.radius||0;n.opacity=e.opacity===undefined?1:e.opacity;parent.appendChild(n);}
if(n){n.x=e.x||0;n.y=e.y||0;}return n;}

const target=await figma.getNodeByIdAsync('3:5');
await figma.setCurrentPageAsync(target);
if(target.children.some(n=>n.name==='Gameplay / UI concept')) return {status:'already-built',nodes:target.children.map(n=>({id:n.id,name:n.name}))};
const concept=await figma.getNodeByIdAsync('3:6');
const result=[];
for(const [index,[name,state]] of Object.entries(spec.states).entries()){
const screen=frame(name==='gameplay'?'Gameplay / UI concept':name==='pause'?'Pause / UI concept':'Completion / UI concept',80+index*1200,120,1080,720,'night');
const bg=record(figma.createRectangle());bg.name='Rooftop concept / raster reference';bg.resize(1080,720);bg.fills=concept.fills;screen.appendChild(bg);
for(const e of state.overlay)build(e,screen);
const heading=tx(name[0].toUpperCase()+name.slice(1)+' / UI concept',24,'ink','Bold');target.appendChild(heading);heading.x=screen.x;heading.y=screen.y-56;
result.push({id:screen.id,name:screen.name,textNodes:screen.findAllWithCriteria({types:['TEXT']}).length});
}
const note=tx('Concept art only. Native safe areas and fold-reserved regions determine final control placement.',20,'ink');note.x=80;note.y=900;
figma.viewport.scrollAndZoomIntoView(target.children.filter(n=>n.type==='FRAME'));
return {createdNodeIds:made,screens:result};

