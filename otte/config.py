import os

redis_host = os.getenv('REDIS_HOST', 'localhost:6379')

REDIS = dict(
        host=redis_host.split(':')[0],
        port=redis_host.split(':')[1],
        db='0',
        password=os.getenv('REDIS_PASSWORD', None),
        socket_timeout=2,
        socket_connect_timeout=2,
        )

COUNTIES = ['baringo', 'bomet', 'bungoma', 'busia',
            'elgeiyo-marakwet', 'embu', 'garissa',
            'homa bay', 'isiolo', 'kajiado', 'kakamega',
            'kericho', 'kiambu', 'kilifi', 'kirinyaga',
            'kisii', 'kisumu', 'kitui', 'kwale', 'laikipia',
            'lamu', 'machakos', 'makueni', 'mandera',
            'marsabit', 'meru', 'migori', 'mombasa',
            "murang'a", 'nairobi', 'nakuru', 'nandi',
            'narok', 'nyamira', 'nyandarua', 'nyeri',
            'samburu', 'siaya', 'taita taveta', 'tana river',
            'tharaka - nithi', 'trans nzoia', 'turkana',
            'uasin gishu', 'vihiga', 'wajir', 'west pokot'
            ]
