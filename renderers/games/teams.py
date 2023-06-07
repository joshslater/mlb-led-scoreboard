import os

from driver import graphics
from PIL import Image

def render_team_banner(
    canvas, layout, team_colors, home_team, away_team, full_team_names, short_team_names_for_runs_hits, show_score 
):
    default_colors = team_colors.color("default")

    away_colors = __team_colors(team_colors, away_team.abbrev)
    try:
        away_team_color = away_colors["home"]
    except KeyError:
        away_team_color = team_colors.color("default.home")

    home_colors = __team_colors(team_colors, home_team.abbrev)
    try:
        home_team_color = home_colors["home"]
    except KeyError:
        home_team_color = team_colors.color("default.home")

    try:
        away_team_accent = away_colors["accent"]
    except KeyError:
        away_team_accent = team_colors.color("default.accent")

    try:
        home_team_accent = home_colors["accent"]
    except KeyError:
        home_team_accent = team_colors.color("default.accent")

    bg_coords = {}
    bg_coords["away"] = layout.coords("teams.background.away")
    bg_coords["home"] = layout.coords("teams.background.home")

    accent_coords = {}
    accent_coords["away"] = layout.coords("teams.accent.away")
    accent_coords["home"] = layout.coords("teams.accent.home")

    for team in ["away", "home"]:
        for x in range(bg_coords[team]["width"]):
            for y in range(bg_coords[team]["height"]):
                color = away_team_color if team == "away" else home_team_color
                x_offset = bg_coords[team]["x"]
                y_offset = bg_coords[team]["y"]
                canvas.SetPixel(x + x_offset, y + y_offset, color["r"], color["g"], color["b"])

    for team in ["away", "home"]:
        for x in range(accent_coords[team]["width"]):
            for y in range(accent_coords[team]["height"]):
                color = away_team_accent if team == "away" else home_team_accent
                x_offset = accent_coords[team]["x"]
                y_offset = accent_coords[team]["y"]
                canvas.SetPixel(x + x_offset, y + y_offset, color["r"], color["g"], color["b"])

    # Draw logos
    team_logos = "assets/team_logos/logos.png"

    logo_order = [
        "AZ",
        "ATL",
        "BAL",
        "BOS",
        "CHC",
        "CWS",
        "CIN",
        "CLE",
        "COL",
        "DET",
        "HOU",
        "KC",
        "LAA",
        "LAD",
        "MIA",
        "MIL",
        "MIN",
        "NYM",
        "NYY",
        "OAK",
        "PHI",
        "PIT",
        "SD",
        "SEA",
        "SF",
        "STL",
        "TB",
        "TEX",
        "TOR",
        "WSH",
    ]

    if os.path.exists(team_logos):
        team_logos = Image.open(team_logos)

        # find the index of the away team in the logo order
        away_logo_index = logo_order.index(away_team.abbrev)

        # calculate the crop box for the away team logo
        crop_box = (
            (away_logo_index % 6) * 16,
            (away_logo_index // 6) * 16,
            (away_logo_index % 6) * 16 + 16,
            (away_logo_index // 6) * 16 + 16,
        )

        away_logo = Image.new('RGB', (16,16), (away_team_color["r"], away_team_color["g"], away_team_color["b"]))
        away_logo.paste(team_logos.crop(crop_box), mask=team_logos.crop(crop_box).split()[3])

        canvas.SetImage(away_logo.convert("RGB"), 0, 0)


        # find the index of the home team in the logo order
        home_logo_index = logo_order.index(home_team.abbrev)

        # calculate the crop box for the home team logo
        crop_box = (
            (home_logo_index % 6) * 16,
            (home_logo_index // 6) * 16,
            (home_logo_index % 6) * 16 + 16,
            (home_logo_index // 6) * 16 + 16,
        )

        home_logo = Image.new('RGB', (16,16), (home_team_color["r"], home_team_color["g"], home_team_color["b"]))
        home_logo.paste(team_logos.crop(crop_box), mask=team_logos.crop(crop_box).split()[3])

        canvas.SetImage(home_logo.convert("RGB"), 0, 16)

        team_logos.close()

    # # image = Image.open('/Users/jslater/Documents/tmp/laa_svg_render.png')

    # image = Image.open('/Users/jslater/Documents/tmp/LAA.png')
    # print(away_team_color)
    # image_bg = Image.new('RGB', image.size, (away_team_color["r"], away_team_color["g"], away_team_color["b"]))

    # # image.thumbnail((16,16))
    # image_bg.paste(image, mask=image.split()[3]) # 3 is the alpha channel

    # # image_bg.thumbnail((16,16))

    # # print(type(matrix))

    # canvas.SetImage(image_bg.convert("RGB"))
    # # canvas.SetPixelsPillow(image.convert("RGB"))

    #     # graphics.VerticalDrawText(canvas, font["font"], coords["x"], coords["y"], text_color_graphic, team_text)



    # image = Image.open('/Users/jslater/Documents/tmp/CHC.png')
    # # image.thumbnail((16,16), resample=Image.NEAREST)
    # image_bg = Image.new('RGB', image.size, (home_team_color["r"], home_team_color["g"], home_team_color["b"]))

    # # image.thumbnail((16,16))
    # image_bg.paste(image, mask=image.split()[3]) # 3 is the alpha channel
    # # print(type(matrix))

    # canvas.SetImage(image_bg.convert("RGB"), 0, 16)
    # # canvas.SetPixelsPillow(image.convert("RGB"))



    use_full_team_names = can_use_full_team_names(
        canvas, full_team_names, short_team_names_for_runs_hits, [home_team, away_team]
    )

# TODO: Support unique score color from team color
    __render_team_text(canvas, layout, away_colors, away_team, "away", use_full_team_names, default_colors )
    __render_team_text(canvas, layout, home_colors, home_team, "home", use_full_team_names, default_colors)

    if show_score:
        # Number of characters in each score.
        score_spacing = {
            "runs": max(len(str(away_team.runs)), len(str(home_team.runs))),
            "hits": max(len(str(away_team.hits)), len(str(home_team.hits))),
            "errors": max(len(str(away_team.errors)), len(str(home_team.errors))),
        }
        __render_team_score(canvas, layout, away_colors, away_team, "away", default_colors, score_spacing)
        __render_team_score(canvas, layout, home_colors, home_team, "home", default_colors, score_spacing)


def can_use_full_team_names(canvas, enabled, abbreviate_on_overflow, teams):
    # Settings enabled and size is able to display it
    if enabled and canvas.width > 32:

        # If config enabled for abbreviating if runs or hits takes up an additional column (i.e. 9 -> 10)
        if abbreviate_on_overflow:

            # Iterate through the teams to see if we should abbreviate
            for team in teams:
                if team.runs > 9 or team.hits > 9:
                    return False

            # Else use full names if no stats column has overflowed
            return True

        # If config for abbreviating is not set, use full name
        else:
            return True

    # Fallback to abbreviated names for all cases
    return False


def __team_colors(team_colors, team_abbrev):
    try:
        team_colors = team_colors.color(team_abbrev.lower())
    except KeyError:
        team_colors = team_colors.color("default")
    return team_colors


def __render_team_text(canvas, layout, colors, team, homeaway, full_team_names, default_colors):
    text_color = colors.get("text", default_colors["text"])
    text_color_graphic = graphics.Color(text_color["r"], text_color["g"], text_color["b"])
    coords = layout.coords("teams.name.{}".format(homeaway))
    font = layout.font("teams.name.{}".format(homeaway))
    team_text = "{:3s}".format(team.abbrev.upper())
    if full_team_names:
        team_text = "{:13s}".format(team.name)
    graphics.DrawText(canvas, font["font"], coords["x"], coords["y"], text_color_graphic, team_text)


def __render_score_component(canvas, layout, colors, homeaway, default_colors, coords, component_val, width_chars):
    # The coords passed in are the rightmost pixel.
    font = layout.font(f"teams.runs.{homeaway}")
    font_width = font["size"]["width"]
    # Number of pixels between runs/hits and hits/errors.
    rhe_coords = layout.coords("teams.runs.runs_hits_errors")
    text_color = colors.get("text", default_colors["text"])
    text_color_graphic = graphics.Color(text_color["r"], text_color["g"], text_color["b"])
    component_val = str(component_val)
    # Draw each digit from right to left.
    for i, c in enumerate(component_val[::-1]):
        if i > 0 and rhe_coords["compress_digits"]:
            coords["x"] += 1
        char_draw_x = coords["x"] - font_width * (i + 1)  # Determine character position
        graphics.DrawText(canvas, font["font"], char_draw_x, coords["y"], text_color_graphic, c)
    if rhe_coords["compress_digits"]:
        coords["x"] += width_chars - len(component_val)  # adjust for compaction on values not rendered
    coords["x"] -= font_width * width_chars + rhe_coords["spacing"] - 1  # adjust coordinates for next score.


def __render_team_score(canvas, layout, colors, team, homeaway, default_colors, score_spacing):
    coords = layout.coords(f"teams.runs.{homeaway}").copy()
    if layout.coords("teams.runs.runs_hits_errors")["show"]:
        __render_score_component(
            canvas, layout, colors, homeaway, default_colors, coords, team.errors, score_spacing["errors"]
        )
        __render_score_component(
            canvas, layout, colors, homeaway, default_colors, coords, team.hits, score_spacing["hits"]
        )
    __render_score_component(canvas, layout, colors, homeaway, default_colors, coords, team.runs, score_spacing["runs"])
