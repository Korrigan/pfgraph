
class UnpackableMixin(object):
    """
    This mixin class provides a classmethod from_data to unpack raw data
    into a python object.

    There is some requirements:
     - child class MUST define a format string for unpack in the class
       attribute "unpack_format" (see the struct module documentation)
     - child class __init__ method MUST take his parameters in the same
       order and in the same number that when returned from unpack

    """
    @classmethod
    def get_unpack_format(cls):
        """
        This method returns the format string to be passed to unpack
        method

        Child classes MUST define cls.unpack_format or override this
        method

        """
        return cls.unpack_format

    @classmethod
    def from_data(cls, data, *extra):
        """
        This method return a tuple containing:
         - an instance of child from the raw network data
         - a string containing the remaining data

        *extra is the extra args to pass to cls.__init__ and will be
        added at the end of args returned by unpack

        """
        from struct import Struct

        st = Struct(cls.get_unpack_format())
        raw = data[0:st.size]
        data = data[st.size:len(data)]
        args = st.unpack(raw)
        args += extra
        instance = cls(*args)
        return (instance, data)

    @classmethod
    def get_cstruct_size(cls):
        """
        Returns the size of the data that will be extracted when
        unpacking.

        """
        from struct import calcsize

        return calcsize(cls.get_unpack_format())


class MetricCollectorMixin(object):
    """
    This mixin class provides helper methods to retrieve metrics in an abstract
    way.

    """

    def get_wanted_metrics(self):
        """
        This method returns a dict (self.wanted_metrics by default) containing
        all metrics name and their equivalent attribute or callable.
        Users of this mixin must define self.wanted metrics or override this
        method.

        """
        return self.wanted_metrics

    def collect_metrics(self):
        """
        Uses self.get_wanted_metrics and returns a dict with the metrics name
        and their values if found

        """
        import inspect

        metrics = {}
        for (k, v) in self.get_wanted_metrics().iteritems():
            if inspect.isfunction(v):
                metrics[k] = v()
            elif hasattr(self, v):
                metrics[k] = getattr(self, v)
        return metrics
