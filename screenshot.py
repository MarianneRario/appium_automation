def get_screen(filename, screenshot):
    with open('static/img/'+str(filename)+'.png', 'wb') as f:
        f.write(screenshot)
        print('Saved screenshot!')
