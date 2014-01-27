require.config
    baseUrl: '/static/tic-tac-toe/js/'

    paths:
        'jquery': [
            '//ajax.googleapis.com/ajax/libs/jquery/1.10.2/jquery.min'
            '../third-party/jquery/jquery'
        ]
        'backbone': '../../third-party/backbone/backbone-min'
        'underscore': '../../third-party/underscore/underscore-min',
        'game': 'game'

    shim:
        'jquery':
            exports: '$'
        'backbone':
            deps: ['jquery', 'underscore']
            exports: 'Backbone'
        'underscore':
            exports: '_'