# - *- coding: utf- 8 - *-
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
from tgbot.data.config import db
from tgbot.data.config import lang_ru as texts
from tgbot.services.crystal import CrystalPay
from tgbot.services.lolz import Lolz
from tgbot.services.payok import PayOk
from tgbot.services.crypto_bot import CryptoBot
from tgbot.services.aaio import Aaio
from tgbot.keyboards.inline_admin import payments_settings_info, payments_settings, payments_back
from tgbot.filters.filters import IsAdmin
from tgbot.data.loader import dp
from tgbot.data import config

try:
    aaio = Aaio(config.aaio_api_key, config.aaio_id_shop, config.aaio_secret_key_1)
    crystal = CrystalPay(config.crystal_Cassa, config.crystal_Token)
    lzt = Lolz(config.lolz_token)
    payok = PayOk(
        api_id=config.payok_api_id,
        api_key=config.payok_api_key,
        secret=config.payok_secret,
        shop_id=config.payok_shop_id
    )
    crypto = CryptoBot(config.crypto_bot_token)
except:
    pass


@dp.callback_query_handler(IsAdmin(), text='payments', state="*")
async def payments_settings_choose(call: CallbackQuery, state: FSMContext):
    await state.finish()

    await call.message.edit_text("<b>⚙️ Выберите способ оплаты</b>", reply_markup=payments_settings())


@dp.callback_query_handler(IsAdmin(), text_startswith="payments:", state="*")
async def payments_info(call: CallbackQuery, state: FSMContext):
    await state.finish()
    way = call.data.split(":")[1]
    s = await db.get_payments()
    def pay_info(way, status):
        if status == "True":
            status = "✅ Включен"
        elif status == "False":
            status = "❌ Выключен"

        msg = f"""
<b>{way}

Статус: <code>{status}</code></b>
"""
        return msg

    if way == "lzt":
        ways = texts.lzt_text
        status = s['pay_lolz']

        await call.message.edit_text(pay_info(ways, status), reply_markup=payments_settings_info(way, status))
    elif way == "crystalPay":
        ways = texts.crystalPay_text
        status = s['pay_crystal']

        await call.message.edit_text(pay_info(ways, status), reply_markup=payments_settings_info(way, status))
    elif way == "cryptoBot":
        ways = texts.cryptoBot_text
        status = s['pay_crypto']

        await call.message.edit_text(pay_info(ways, status), reply_markup=payments_settings_info(way, status))
    elif way == "payok":
        ways = texts.payok_text
        status = s['pay_payok']

        await call.message.edit_text(pay_info(ways, status), reply_markup=payments_settings_info(way, status))
    elif way == 'aaio':
        ways = texts.aaio_text
        status = s['pay_aaio']

        await call.message.edit_text(pay_info(ways, status), reply_markup=payments_settings_info(way, status))


@dp.callback_query_handler(IsAdmin(), text_startswith="payments_on_off:", state="*")
async def off_payments(call: CallbackQuery):

    way = call.data.split(":")[1]
    action = call.data.split(":")[2]
    def pay_info(way, status):
        if status == "True":
            status = "✅ Включен"
        elif status == "False":
            status = "❌ Выключен"

        msg = f"""
<b>{way}

Статус: <code>{status}</code></b>
    """
        return msg

    if way == "lzt":
        ways = texts.lzt_text

        if action == "off":
            await db.update_payments(pay_lolz="False")
        else:
            await db.update_payments(pay_lolz="True")

        s = await db.get_payments()
        status = s['pay_lolz']

        await call.message.edit_text(pay_info(ways, status), reply_markup=payments_settings_info(way, status))
    elif way == "crystalPay":
        ways = texts.crystalPay_text

        if action == "off":
            await db.update_payments(pay_crystal="False")
        else:
            await db.update_payments(pay_crystal="True")

        s = await db.get_payments()
        status = s['pay_crystal']

        await call.message.edit_text(pay_info(ways, status), reply_markup=payments_settings_info(way, status))
    elif way == "cryptoBot":
        ways = texts.cryptoBot_text

        if action == "off":
            await db.update_payments(pay_crypto="False")
        else:
            await db.update_payments(pay_crypto="True")

        s = await db.get_payments()
        status = s['pay_crypto']

        await call.message.edit_text(pay_info(ways, status), reply_markup=payments_settings_info(way, status))
    elif way == "payok":
        ways = texts.payok_text

        if action == "off":
            await db.update_payments(pay_payok="False")
        else:
            await db.update_payments(pay_payok="True")

        s = await db.get_payments()
        status = s['pay_payok']

        await call.message.edit_text(pay_info(ways, status), reply_markup=payments_settings_info(way, status))
    elif way == "aaio":
        ways = texts.aaio_text

        if action == "off":
            await db.update_payments(pay_aaio="False")
        else:
            await db.update_payments(pay_aaio="True")

        s = await db.get_payments()
        status = s['pay_aaio']

        await call.message.edit_text(pay_info(ways, status), reply_markup=payments_settings_info(way, status))


@dp.callback_query_handler(IsAdmin(), text_startswith="payments_balance:", state="*")
async def payments_balance_call(call: CallbackQuery, state: FSMContext):
    await state.finish()
    way = call.data.split(":")[1]

    if way == "crystalPay":
        ways = texts.crystalPay_text

        balance = await crystal.get_balance()

        await call.message.edit_text(f"{ways} \n\n{balance}", reply_markup=payments_back())
    elif way == "lzt":
        ways = texts.lzt_text
        data = await lzt.get_user()
        balance = data['balance']
        hold = data['hold']

        await call.message.edit_text(f'{ways} \n\nВаш баланс: <code>{balance+hold} RUB</code> (<code>{hold} RUB</code> в холде)', reply_markup=payments_back())
    elif way == "payok":
        ways = texts.payok_text

        balance = await payok.get_balance()

        await call.message.edit_text(f"{ways} \n\nВаш баланс: {balance}", reply_markup=payments_back())
    elif way == "cryptoBot":
        ways = texts.cryptoBot_text

        balance = await crypto.get_balance()
        bal = ""
        for ball in balance['result']:
            bal += f"<b>{ball['currency_code']}: <code>{round(float(ball['available']), 2)} {ball['currency_code']}</code></b>\n"

        await call.message.edit_text(text=f"{ways} \n\nВаш баланс: \n{bal}", reply_markup=payments_back())

    elif way == "aaio":
        ways = texts.aaio_text
        balance = await aaio.get_balance()

        await call.message.edit_text(text=f"{ways} \n\nВаш баланс: \n{balance['balance']}₽ (В холде: {balance['hold']}₽)",
                                     reply_markup=payments_back())


@dp.callback_query_handler(IsAdmin(), text_startswith="payments_info:", state="*")
async def payments_info_open(call: CallbackQuery, state: FSMContext):
    await state.finish()

    way = call.data.split(":")[1]

    if way == "crystalPay":
        ways = texts.crystalPay_text

        await call.message.edit_text(f"{ways} \n\nЛогин кассы: <code>{config.crystal_Cassa}</code> \nСекретный токен 1: <code>{config.crystal_Token}</code>", reply_markup=payments_back())

    elif way == "lzt":
        ways = texts.lzt_text

        await call.message.edit_text(f"{ways} \n\nТокен: <code>{config.lolz_token}</code> \nНик: <code>{config.lolz_nick}</code> \nID: <code>{config.lolz_id}</code>", reply_markup=payments_back())
    elif way == "payok":
        ways = texts.payok_text

        await call.message.edit_text(f"{ways} \n\nТокен: <code>{config.payok_api_key}</code> \nAPI ID: <code>{config.payok_api_id}</code> \nID Магазина: <code>{config.payok_shop_id}</code> \nСекретный ключ: <code>{config.payok_secret}</code>", reply_markup=payments_back())
    elif way == "cryptoBot":
        ways = texts.cryptoBot_text

        await call.message.edit_text(f"{ways} \n\nТокен: <code>{config.crypto_bot_token}</code>", reply_markup=payments_back())
    elif way == "aaio":
        ways = texts.aaio_text

        await call.message.edit_text(f"{ways} \n\nAPI-Ключ: <code>{config.aaio_api_key}</code> \nID Магазина: <code>{config.aaio_id_shop}</code> \nСекретный ключ 1: <code>{config.aaio_secret_key_1}</code>", reply_markup=payments_back())