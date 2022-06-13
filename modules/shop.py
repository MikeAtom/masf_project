name = 'Shop'
emodji = '🏪'
mod_id = 'shop_gradwork'
author = 'me'
desc = "Furniture shop for your house or office."
version = 0
button = 'Shop'

item_dir = 'files/shop/items/'
order_dir = 'files/shop/orders/'
cart_dir = 'files/shop/cart'

master_id = [379811871]


def loaded():
    return name + ' is loaded!'


def logic(user_id, content, content_type, full_message, caption):
    from data.scripts.send_message import send_message, delete_message
    from data.scripts.save_file import save_file
    from data.handlers.userhand import write_profile, read_profile
    from data.handlers.datahand import create_data, read_data, write_data
    from data.scripts.dir_search import dir_search
    from data.scripts.dir_count import dir_count

    global products
    products = dir_search(item_dir, '*.item')

    def read_cart(user_id):
        try:
            cart = read_data(cart_dir, str(user_id))
        except:
            cart = ''
        return cart

    def write_cart(user_id, cart):
        write_data(cart_dir, user_id, cart)

    def get_order_price(user_id):
        order_list = read_cart(user_id).split(',')
        price = 0
        for item in order_list:
            for product in products:
                if item == product:
                    price += int(int(read_data(item_dir + product, 'price')) * (
                            100 - int(read_data(item_dir + product, 'sale'))) / 100)
        return str(price)

    def phase(value):
        write_profile(user_id, 'Shop', 'phase', value)

    if user_id in master_id:
        try:
            if read_profile(user_id, 'Shop', 'mode') == '':
                write_profile(user_id, 'Shop', 'mode', 'admin')
        except:
            write_profile(user_id, 'Shop', 'mode', 'admin', section_create=True)
            write_profile(user_id, 'Shop', 'phase', '')

        if content == '$mode':
            phase('')
            if read_profile(user_id, 'Shop', 'mode') == 'admin':
                write_profile(user_id, 'Shop', 'mode', 'user')
                send_message(user_id, 'Mode changed to user')
            else:
                write_profile(user_id, 'Shop', 'mode', 'admin')
                send_message(user_id, 'Mode changed to admin')
                logic(user_id, '', '', '', '')

    if read_profile(user_id, 'Shop', 'mode') == 'admin':
        if content == '$add':
            global cur_item
            cur_item = 'product-' + str(dir_count(item_dir))
            create_data(item_dir + cur_item, ['name', 'desc', 'price', 'stock', 'sale'])
            phase('add')
            send_message(user_id, 'Send item photo as document')
        elif content == '$remove':
            phase('remove')
            send_message(user_id, 'Send item name')
        elif content == '$edit':
            phase('edit')
            send_message(user_id, 'Send item name')
        elif content == '$list':
            phase('list')
            for product in products:
                send_message(user_id, content_type='document', content=item_dir + product + '.jpg',
                             caption='id: ' + product + '\n\nname: ' + read_data(item_dir + product,
                                                                                 'name') + '\n\ndesc: ' + read_data(
                                 item_dir + product, 'desc') + '\n\nprice: ' + read_data(item_dir + product,
                                                                                         'price') + '\n\nstock: ' + read_data(
                                 item_dir + product, 'stock') + '\n\nsale: ' + read_data(item_dir + product, 'sale'))
        elif content == '$cancel':
            phase('')
            send_message(user_id, 'Canceled')
        if read_profile(user_id, 'Shop', 'phase') == 'add':
            if content_type == 'document':
                save_file(full_message, item_dir, cur_item, 'jpg')
                send_message(user_id, 'Send item name')
                phase('add_name')
        if read_profile(user_id, 'Shop', 'phase') == 'add_name':
            if content_type == 'text':
                write_data(item_dir + cur_item, 'name', content)
                phase('add_desc')
                send_message(user_id, 'Send item description')
        elif read_profile(user_id, 'Shop', 'phase') == 'add_desc':
            if content_type == 'text':
                write_data(item_dir + cur_item, 'desc', content)
                phase('add_price')
                send_message(user_id, 'Send item price')
        elif read_profile(user_id, 'Shop', 'phase') == 'add_price':
            if content_type == 'text':
                write_data(item_dir + cur_item, 'price', content)
                phase('add_stock')
                send_message(user_id, 'Send item stock')
        elif read_profile(user_id, 'Shop', 'phase') == 'add_stock':
            if content_type == 'text':
                write_data(item_dir + cur_item, 'stock', content)
                phase('add_sale')
                send_message(user_id, 'Send item sale')
        elif read_profile(user_id, 'Shop', 'phase') == 'add_sale':
            if content_type == 'text':
                write_data(item_dir + cur_item, 'sale', content)
                phase('')
                send_message(user_id, 'Item added')
        elif read_profile(user_id, 'Shop', 'phase') == 'remove':
            if content_type == 'text':
                try:
                    from os import remove
                    remove(item_dir + content + '.item')
                    send_message(user_id, 'Item removed')
                except:
                    send_message(user_id, 'Item not found')
        elif read_profile(user_id, 'Shop', 'phase') == 'edit':
            if content_type == 'text':
                try:
                    cur_item = content
                    phase('edit_photo')
                    send_message(user_id, 'Send item name')
                except:
                    send_message(user_id, 'Item not found')
        elif read_profile(user_id, 'Shop', 'phase') == 'edit_photo':
            if content_type == 'document':
                save_file(full_message, item_dir, cur_item, 'jpg')
                phase('edit_name')
                send_message(user_id, 'Send item name')
        elif read_profile(user_id, 'Shop', 'phase') == 'edit_name':
            if content_type == 'text':
                if content != '-':
                    write_data(item_dir + cur_item, 'name', content)
                phase('edit_desc')
                send_message(user_id, 'Send item description')
        elif read_profile(user_id, 'Shop', 'phase') == 'edit_desc':
            if content_type == 'text':
                if content != '-':
                    write_data(item_dir + cur_item, 'desc', content)
                phase('edit_price')
                send_message(user_id, 'Send item price')
        elif read_profile(user_id, 'Shop', 'phase') == 'edit_price':
            if content_type == 'text':
                if content != '-':
                    write_data(item_dir + cur_item, 'price', content)
                phase('edit_stock')
                send_message(user_id, 'Send item stock')
        elif read_profile(user_id, 'Shop', 'phase') == 'edit_stock':
            if content_type == 'text':
                if content != '-':
                    write_data(item_dir + cur_item, 'stock', content)
                phase('edit_sale')
                send_message(user_id, 'Send item sale')
        elif read_profile(user_id, 'Shop', 'phase') == 'edit_sale':
            if content_type == 'text':
                if content != '-':
                    write_data(item_dir + cur_item, 'sale', content)
                phase('')
                send_message(user_id, 'Item edited')
        elif read_profile(user_id, 'Shop', 'phase') == 'list':
            if content_type == 'text':
                if content == '$cancel':
                    phase('')
                    send_message(user_id, 'Canceled')
        #get list of all orders with customer phone number and address and order price
        elif content == '$orders':
            for order in dir_search(order_dir, '*.item'):
                order_price = read_data(order_dir + order, 'price')
                order_phone = read_data(order_dir + order, 'phone')
                order_address = read_data(order_dir + order, 'address')
                order_date = read_data(order_dir + order, 'date')
                send_message(user_id, 'Order id: ' + order + '\n\nPrice: ' + order_price + '\n\nPhone: ' + order_phone + '\n\nAddress: ' + order_address + '\n\nDate: ' + order_date)
        elif content == '$help':
            send_message(user_id, '$help - show this menu\n\n$orders - show all orders\n\n$cancel - cancel current operation\n\n$add - add new item\n\n$remove - remove item\n\n$edit - edit item\n\n$list - show list of items')


    if (not user_id in master_id) or (user_id in master_id and read_profile(user_id, 'Shop', 'mode') == 'user'):

        create_data(cart_dir, [])

        try:
            phase(read_profile(user_id, 'Shop', 'phase'))
        except:
            write_profile(user_id, 'Shop', 'phase', '', section_create=True)

        if read_profile(user_id, 'Shop', 'phase') == '':
            product_buttons = []

            for product in products:
                # create_data('files/shop/items/' + product, ['name', 'desc', 'price', 'stock', 'sale'])
                product_buttons.append([read_data(item_dir + product, 'name'), product])
            send_message(user_id, 'Наш каталог', keyboard='reply', buttons=['Кошик'])
            send_message(user_id, 'files/shop/logo.jpg', content_type='photo', caption='', keyboard='inline',
                         buttons=product_buttons)
            phase('product_info')

        elif read_profile(user_id, 'Shop', 'phase') == 'product_info':
            if content == 'Кошик':
                # never gonna give you up
                # never gonna let you down
                # never gonna run around and desert you
                # never gonna make you cry
                # never gonna say goodbye
                # never gonna tell a lie and hurt you

                if read_cart(user_id) == '':
                    send_message(user_id, 'Кошик порожній')
                    phase('')
                    logic(user_id, '', '', '', '')
                else:
                    order_list = read_cart(user_id).split(',')

                    for item in order_list:
                        for product in products:
                            if item == product:
                                send_message(user_id, 'files/shop/items/' + product + '.jpg', content_type='photo',
                                             caption=read_data(item_dir + product, 'name') + '\n' + read_data(
                                                 item_dir + product,
                                                 'desc') + '\n' + 'Ціна: ' + str(
                                                 int(int(read_data(item_dir + product, 'price')) * (
                                                         100 - int(read_data(item_dir + product, 'sale'))) / 100)) + '\n',
                                             keyboard='inline', buttons=[['Видалити', item + ',' + str(full_message.id)]])
                    phase('cart')
                    send_message(user_id, 'Ваш кошик на суму: ' + get_order_price(user_id), keyboard='inline',
                                 buttons=[['Оплатити', 'buy'], ['Очистити', 'clear'],
                                          ['Назад', 'back']])

            for product in products:
                if content == product:
                    buttons = [['До кошика', product], ['Назад', 'back']]
                    send_message(user_id, 'files/shop/items/' + product + '.jpg', content_type='photo',
                                 caption=read_data(item_dir + product, 'name') + '\n' + read_data(item_dir + product,
                                                                                                  'desc') + '\n' + 'Ціна: ' + str(
                                     int(int(read_data(item_dir + product, 'price')) * (
                                             100 - int(read_data(item_dir + product, 'sale'))) / 100)) + '\n',
                                 keyboard='inline', buttons=buttons)
                    phase('product')
                    break

        elif read_profile(user_id, 'Shop', 'phase') == 'product':
            if content == 'back':
                phase('')
                logic(user_id, '', '', '', '')
            elif content[0] == 'p':
                phase('')
                write_cart(str(user_id), read_cart(user_id) + ',' + content)
                logic(user_id, content, content_type, full_message, caption)

        elif read_profile(user_id, 'Shop', 'phase') == 'cart':
            if content == 'back':
                phase('')
                logic(user_id, '', '', '', '')
            elif content == 'buy':
                create_data(order_dir + str(user_id), ['phone', 'address', 'order'])
                write_data(order_dir + str(user_id), 'order', read_cart(user_id))
                phase('order_phone')
                send_message(user_id, 'Введіть номер телефону: ', keyboard='inline', buttons=[['Відмінити', 'back']])
            elif content == 'clear':
                write_cart(str(user_id), '')
                send_message(user_id, 'Кошик очищено')
                phase('')
                logic(user_id, '', '', '', '')
            elif content[0] == 'p':
                delete_message(user_id, full_message.message.id)
                order_list = read_cart(user_id).split(',')
                order_list.remove(content.split(',')[0])
                write_cart(str(user_id), ','.join(order_list))


        elif read_profile(user_id, 'Shop', 'phase') == 'order_phone':
            if content == 'back':
                phase('')
                logic(user_id, '', '', '', '')
            else:
                write_data(order_dir + str(user_id), 'phone', content)
                phase('order_address')
                send_message(user_id, 'Введіть адресу: ', keyboard='inline', buttons=[['Відмінити', 'back']])

        elif read_profile(user_id, 'Shop', 'phase') == 'order_address':
            if content == 'back':
                phase('')
                logic(user_id, '', '', '', '')
            else:
                write_data(order_dir + str(user_id), 'address', content)
                phase('order_confirm')
                logic(user_id, '', '', '', '')


        elif read_profile(user_id, 'Shop', 'phase') == 'order_confirm':
            send_message(user_id,'Ваш номер телефону: ' + read_data(order_dir + str(user_id), 'phone') + '\n' + 'Ваша адреса: ' + read_data(order_dir + str(user_id), 'address') + '\n' + 'Сума замовлення: ' + get_order_price(user_id) + '\n' + 'Підтвердити замовлення?', keyboard='inline', buttons=[['Так', 'confirm'], ['Ні', 'back']])
            if content == 'confirm':
                from datetime import datetime
                write_data(order_dir + str(user_id), 'time', str(datetime.now()))
                write_data(order_dir + str(user_id), 'price', get_order_price(user_id))
                write_cart(str(user_id), '')

                phase('order_success')
                logic(user_id, '', '', '', '')
            elif content == 'back':
                phase('order_phone')
                logic(user_id, '', '', '', '')
        elif read_profile(user_id, 'Shop', 'phase') == 'order_success':
            send_message(user_id, 'Ваше замовлення прийнято!')
            phase('')
            logic(user_id, '', '', '', '')
