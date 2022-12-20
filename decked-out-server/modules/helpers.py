#!/usr/bin/env python3

# Helper Functions

def get_keys_nested_dict(lst):
    '''Get all keys from an arbitrarly deeply nested dictionary'''
    main_points = []
    for slide in lst:
        key = list(slide.keys())[0]

        main_points.append(slide[key])

    return main_points
