import flet as ft 
from db import main_db

def main(page: ft.Page):
    page.title = 'Список покупок'
    page.theme_mode = ft.ThemeMode.LIGHT
    product_list = ft.Column(spacing=20)
    filter_type = 'all'
    purchased_products = ft.Text(value='Купленных продуктов: 0')

    def load_product():
        product_list.controls.clear()
        purchased_amount = 0
        for product_id, product_text, purchased in main_db.get_product(filter_type):
            product_list.controls.append(create_product_row(product_id=product_id, product_text=product_text, purchased=purchased))
            if purchased:
                purchased_amount += 1
        purchased_products.value = f'Купленных продуктов: {purchased_amount}'
        page.update()

    def create_product_row(product_id, product_text, purchased):
        checkbox = ft.Checkbox(value=bool(purchased), on_change=lambda e: toggle_product(product_id, e.control.value))

        def delete_product(_):
            main_db.delete_product(product_id=product_id)
            load_product()
            
        delete_button = ft.IconButton(icon=ft.Icons.DELETE_OUTLINE, icon_color=ft.Colors.RED, on_click=delete_product)
        product_field = ft.TextField(value=product_text, expand=True)
        return ft.Row([checkbox, product_field, delete_button])

    def toggle_product(product_id, is_purchased):
        print(f'{product_id} - {is_purchased}')
        main_db.update_product(product_id=product_id, purchased=int(is_purchased))
        load_product()

    def add_product(_):
        if product_input.value:
            product = product_input.value
            product_id = main_db.add_product(product)
            product_list.controls.append(create_product_row(product_id=product_id, product_text=product, purchased=None))
            print(f'Запись сохранена! ID продукта - {product_id}')
            product_input.value = None
            page.update()

    product_input = ft.TextField(label='Введите наименование продукта:', expand=True, on_submit=add_product)
    product_input_button = ft.IconButton(icon=ft.Icons.ADD, on_click=add_product)

    main_objects = ft.Row([product_input, product_input_button])

    def set_filter(filter_value):
        nonlocal filter_type
        filter_type = filter_value
        load_product()

    filter_buttons = ft.Row([
        ft.ElevatedButton('Все продукты', on_click=lambda e: set_filter('all'), icon=ft.Icons.ALL_INBOX_OUTLINED, icon_color=ft.Colors.BLUE),
        ft.ElevatedButton('Некупленные', on_click=lambda e: set_filter('nonpurchased'), icon=ft.Icons.WATCH_LATER, icon_color=ft.Colors.RED),
        ft.ElevatedButton('Купленные', on_click=lambda e: set_filter('purchased'), icon=ft.Icons.CHECK_BOX, icon_color=ft.Colors.GREEN)
    ], alignment=ft.MainAxisAlignment.SPACE_EVENLY)

    def delete_purchased(_):
        main_db.delete_product()
        load_product()
    
    delete_button = ft.ElevatedButton('Удалить все купленные', icon=ft.Icons.DELETE_SWEEP, icon_color=ft.Colors.RED, on_click=delete_purchased)

    page.add(main_objects, filter_buttons, purchased_products, product_list,delete_button)
    load_product()



if __name__ == '__main__':
    main_db.init_db()
    ft.app(target=main)