

def widget_switching(main_window, current_widget, switched_widget, *args):
    # 이전 위젯 삭제  
    if current_widget != None:
        del current_widget
    # 새로 받은 위젯 적용 
    if switched_widget == "main_view":
        from view.main_view import MainWidget
        current_widget = MainWidget(main_window, args)
    elif switched_widget == "settings_view": 
        from view.settings_view import SettingWidget
        current_widget = SettingWidget(main_window, args)
    elif switched_widget == "draw_line_view": 
        # current_widget = MainWidget(main_window, args)
        pass 
    main_window.setCentralWidget(current_widget)