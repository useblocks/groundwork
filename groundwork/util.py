def gw_get(object_dict, name=None, plugin=None):
    """
    Getter function to retrieve objects from a given object dictionary.

    Used mainly to provide get() inside patterns.

    :param object_dict: objects, which must have 'name' and 'plugin' as attribute
    :type object_dict: dictionary
    :param name: name of the object
    :type name: str
    :param plugin: plugin name, which registers the object
    :return: None, single object or dict of objects
    """
    if plugin is not None:
        if name is None:
            object_list = {}
            for key in object_dict.keys():
                if object_dict[key].plugin == plugin:
                    object_list[key] = object_dict[key]
            return object_list
        else:
            if name in object_dict.keys():
                if object_dict[name].plugin == plugin:
                    return object_dict[name]
                else:
                    return None
            else:
                return None
    else:
        if name is None:
            return object_dict
        else:
            if name in object_dict.keys():
                return object_dict[name]
            else:
                return None
