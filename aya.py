from ghost import Ghost

ghost = Ghost()
page, extra_resources =\
    ghost.open('http://online.konzum.hr/#!/categories/60004323/hrana?show=all&sort_field=name&sort=nameAsc&max_price=300&page=1&per_page=200')
page, extra_resources = ghost.wait_for_page_loaded('http://online.konzum.hr/#!/categories/60004323/hrana?show=all&sort_field=name&sort=nameAsc&max_price=300&page=1&per_page=200')
f = open('fajl', 'w')
f.write(page.content)
f.close()
