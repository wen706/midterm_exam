import pack.modu as lib

lib.顯示書籍()
lib.偵測()
while True:
    break
    if lib.登入()==True:
        break
while True:
    lib.選單()
    cmd=input("選擇要執行的功能(Enter離開)：")
    if cmd=="1":
        try:
            lib.增加記錄()
        except ValueError as e:
            print(e)
        except Exception as e:
            print('未知錯誤...')
            print(f'錯誤代碼為：{e.errno}')
            print(f'錯誤訊息為：{e.strerror}')
            print(f'錯誤檔案為：{e.filename}')
    elif cmd=="2":
        try:
            lib.刪除紀錄()
        except ValueError as e:
            print(e)
        except Exception as e:
            print('未知錯誤...')
            print(f'錯誤代碼為：{e.errno}')
            print(f'錯誤訊息為：{e.strerror}')
            print(f'錯誤檔案為：{e.filename}')
    elif cmd=="3":
        try:
            lib.修改紀錄()
        except ValueError as e:
            print(e)
        except Exception as e:
            print('未知錯誤...')
            print(f'錯誤代碼為：{e.errno}')
            print(f'錯誤訊息為：{e.strerror}')
            print(f'錯誤檔案為：{e.filename}')   
    elif cmd=="4":
        try:
            lib.查詢()
        except ValueError as e:
            print(e)
        except Exception as e:
            print('未知錯誤...')
            print(f'錯誤代碼為：{e.errno}')
            print(f'錯誤訊息為：{e.strerror}')
            print(f'錯誤檔案為：{e.filename}')
    elif cmd=="5":
        try:
            lib.顯示書籍()
        except ValueError as e:
            print(e)
        except Exception as e:
            print('未知錯誤...')
            print(f'錯誤代碼為：{e.errno}')
            print(f'錯誤訊息為：{e.strerror}')
            print(f'錯誤檔案為：{e.filename}')
    elif cmd=="":
        break
    else:
        print("=>無效的選擇")
    