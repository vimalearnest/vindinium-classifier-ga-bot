class Message:
    def __init__(self,game):
        self.status = []

        # Hero stats indexes 0, 1
        self.status.append( int( ( game.hero.life / 100.0 ) * 6 - 0.01) )
        self.status.append( int( ( game.hero.mines / float(len( game.board.mines )) ) * 6 - 0.01) )
  
        # Enemy stats  0 = distance, 1 = health, 2 = mines
        # Closest Enemy indexes  2, 3, 4,
        # Enemy 2 indexes        5, 6, 7,
        # Farthest Enemy indexes 8, 9, 10,
        enemy_status = [] 
        i = 0
        for pos,enemy in game.enemies.iteritems():
            if ( None == enemy.path):
                distance = 999
            else:
                distance = len(enemy.path)
            enemy_status.append([])
            enemy_status[i].append(distance)
            enemy_status[i].append([])
            if ( distance < 2 ):
                enemy_status[i][1].append(0)
            elif ( distance < 4 ):
                enemy_status[i][1].append(1)
            elif ( distance < 8 ):
                enemy_status[i][1].append(2)
            elif ( distance < 16 ):
                enemy_status[i][1].append(3)
            elif ( distance < 32 ):
                enemy_status[i][1].append(4)
            else:
                enemy_status[i][1].append(5)
            enemy_status[i][1].append( int( ( enemy.life / 100.0 ) * 6 - 0.01) )
            enemy_status[i][1].append( int( ( enemy.mines / float(len( game.board.mines )) ) * 6 - 0.01) )
            i += 1
        enemy_status.sort()
        for enemy in enemy_status:
            self.status.extend(enemy[1])
        print self.status
    def rule_matches(self,classifier):
        i = 0
        for x in classifier.rule:
            if ( None != x ):
                if ( self.status[i] not in x ):
                    return False
            i += 1
        return True
                
