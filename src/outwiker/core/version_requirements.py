from typing import List, Iterable


class Requirements:
    """
    Plug-in's requirements
    """

    def __init__(self,
                 os_list: List[str],
                 api_list: List[Iterable[int]]):
        """
        os_list - list of the supported OS
        api_list - list of Version instances with supported API versions.
        """
        self.os_list = os_list[:]
        self.api_list = api_list[:]
