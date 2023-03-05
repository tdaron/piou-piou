end = False
res = ''
while end != True:
    file_texture = input('File Texture name (no png no /) : \t')
    speed = input('Speed (vector) : \t')
    damage = input('Damage : \t')
    health = input('Health : \t')
    reload_time = input('Reload_time : \t')
    bullet_speed = input('Bullet speed (vector : \t')
    bullet_sprite = input('Name of the texture of the bullet: ')
    line = 'Assets/Enemy Ships/'+file_texture+'.png:Assets/Projectiles/Projectiles/'+bullet_sprite+'.png:'+bullet_speed+speed+':'+damage+':'+health+':'+reload_time+'\n'
    print(line)
    res+= line
    end = input('Wanna write (y/n) : \t')
    if end == 'y':
        file_name = input('level number : \t')
        with open(rf'C:\Users\Theo\Downloads\PREMS_EXCH\Hackathon proj\levels{file_name}.txt', 'w') as file:
            file.write(res)