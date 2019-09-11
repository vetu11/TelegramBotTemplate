"""
Here should be declared all functions that handle the supported Telegram API calls.
"""

import const
from bot_tokens import PAYMENT_PROVIDER_TOKEN
from lang import get_lang
from telegram import ParseMode, InlineKeyboardMarkup, InlineKeyboardButton, LabeledPrice


def generic_message(bot, update, text_code, **kwargs):
    """Answers the message with a fixed text. Add kwargs to insert text."""
    message = update.effective_message
    lang = get_lang(update.effective_user.language_code)

    message.reply_text(lang.get_text(text_code, **kwargs), parse_mode=ParseMode.MARKDOWN)


def start(bot, update):
    generic_message(bot, update, "start")


def help(bot, update):
    generic_message(bot, update, "help")


def more(bot, update):
    generic_message(bot, update, "more")


def about(bot, update):
    generic_message(bot, update, "about", **{"botusername": bot.username, "version": const.VERSION})


def ping(bot, update):
    update.effective_message.reply_text("Pong!", quote=False)


def donate(bot, update, user_data):
    if PAYMENT_PROVIDER_TOKEN is None:
        generic_message(bot, update, "donations_not_available")
        return

    lang = get_lang(update.effective_user.language_code)

    user_data["donation"] = 5
    text = lang.get_text("donate")
    keyboard = [[InlineKeyboardButton("❤ %s€ ❤" % user_data["donation"], callback_data="donate")],
                [InlineKeyboardButton("⏬", callback_data="don*LLL"),
                 InlineKeyboardButton("⬇️", callback_data="don*LL"),
                 InlineKeyboardButton("🔽", callback_data="don*L"),
                 InlineKeyboardButton("🔼", callback_data="don*G"),
                 InlineKeyboardButton("⬆️", callback_data="don*GG"),
                 InlineKeyboardButton("⏫", callback_data="don*GGG")]]
    update.message.reply_text(text,
                              reply_markup=InlineKeyboardMarkup(keyboard),
                              parse_mode=ParseMode.MARKDOWN,
                              disable_web_page_preview=True)


def change_donation_quantity(bot, update, user_data):

    if "donation" not in user_data:
        user_data["donation"] = 5

    s = update.callback_query.data.split("*")
    change = 5 ** (s[1].count("G") - 1) if "G" in s[1] else -(5 ** (s[1].count("L") - 1))
    user_data["donation"] += change
    if user_data["donation"] < 1:
        user_data["donation"] = 1

    keyboard = [[InlineKeyboardButton("❤ %s€ ❤" % user_data["donation"], callback_data="donate")],
                [InlineKeyboardButton("⏬", callback_data="don*LLL"),
                 InlineKeyboardButton("⬇️", callback_data="don*LL"),
                 InlineKeyboardButton("🔽", callback_data="don*L"),
                 InlineKeyboardButton("🔼", callback_data="don*G"),
                 InlineKeyboardButton("⬆️", callback_data="don*GG"),
                 InlineKeyboardButton("⏫", callback_data="don*GGG")]]

    update.effective_message.edit_reply_markup(reply_markup=InlineKeyboardMarkup(keyboard))
    update.callback_query.answer()


def send_donation_receipt(bot, update, user_data):
    lang = get_lang(update.effective_user.language_code)

    if "donation" not in user_data:
        user_data["donation"] = 5

    title = lang.get_text("donation_title")
    description = lang.get_text("donation_description")
    prices = [LabeledPrice(title, user_data["donation"] * 100)]

    bot.send_invoice(chat_id=update.effective_chat.id,
                     title=title,
                     description=description,
                     payload="approve_donation",
                     provider_token=PAYMENT_PROVIDER_TOKEN,
                     start_parameter="donacion",
                     currency="EUR",
                     prices=prices)
    update.effective_message.edit_reply_markup(reply_markup=InlineKeyboardMarkup([[]]))


def approve_transaction(bot, update):
    query = update.pre_checkout_query

    if query.invoice_payload != 'approve_donation':
        bot.answer_pre_checkout_query(pre_checkout_query_id=query.id, ok=False,
                                      error_message="Algo ha fallado, vuelve a intentarlo por favor.")
    else:
        bot.answer_pre_checkout_query(pre_checkout_query_id=query.id, ok=True)


def completed_donation(bot, update):
    update.effective_message.reply_text("Muchisimas gracias por donar!! ❤️❤️❤️")
    bot.send_message(const.ADMIN_TELEGRAM_ID, "%s ha donado!" % update.effective_user)


def support(bot, update):
    message = update.effective_message
    lang = get_lang(update.effective_user.language_code)

    if len(message.text.replace("/support", "")) > 0:
        message.forward(const.ADMIN_TELEGRAM_ID)
        message.reply_text(lang.get_text("support_sent"))
    else:
        message.reply_text(lang.get_text("support_default"))


def support_group(bot, update):
    generic_message(bot, update, "private_command")


def error(bot, update, error):
    bot.send_message(const.ADMIN_TELEGRAM_ID, "The update:\n%s\nhas caused this error:\n%s" % (str(update), str(error)))
