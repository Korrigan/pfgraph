from .mixins import UnpackableMixin
from .mixins import MetricCollectorMixin


class PFStatus(UnpackableMixin, MetricCollectorMixin):
    """
    A class correspondig to the following C struct:
    struct pf_status {
    u_int64_t       counters[PFRES_MAX];
    u_int64_t       lcounters[LCNT_MAX];    /* limit counters */
    u_int64_t       fcounters[FCNT_MAX];
    u_int64_t       scounters[SCNT_MAX];
    u_int64_t       pcounters[2][2][3];
    u_int64_t       bcounters[2][2];
    u_int64_t       stateid;
    u_int32_t       running;
    u_int32_t       states;
    u_int32_t       src_nodes;
    u_int32_t       since;
    u_int32_t       debug;
    u_int32_t       hostid;
    u_int32_t       reass;                  /* reassembly */
    char            ifname[IFNAMSIZ];
    u_int8_t        pf_chksum[MD5_DIGEST_LENGTH];
    };

    With the following defines:
    #define PFRES_MAX 15
    #define LCNT_MAX 7
    #define FCNT_MAX 3
    #define SCNT_MAX 3
    #define IFNAMSIZE 16
    #define PF_MD5_DIGEST_LENGTH 16

    See OpenBSD sources sys/net/pfvar.h
    
    """
    unpack_format = "@ 15Q 7Q 3Q 3Q 12Q 4Q Q I I I I I I I 16s 16s"

    @classmethod
    def retrieve(cls, device="/dev/pf"):
        """
        Retrieve pf_status struct from device using the DIOCGETSTATUS (3249030165)
        ioctl and unpack it to a cls instance

        """
        import fcntl

        with open(device, 'r') as dev:
            status = fcntl.ioctl(dev, 3249030165, "0" * cls.get_cstruct_size())
            instance, data = cls.from_data(status)
            return instance

    def __init__(self,
                 count_match,
                 count_bad_offset,
                 count_fragmented,
                 count_short,
                 count_normalized,
                 count_memory,
                 count_bad_timestamp,
                 count_congest,
                 count_ip_opts,
                 count_bad_checksum,
                 count_bad_state,
                 count_state_insert,
                 count_max_states,
                 count_max_source,
                 count_synproxy,
                 limit_state,
                 limit_source_state,
                 limit_source_node,
                 limit_source_conn,
                 limit_source_conn_rate,
                 overload_table_insert,
                 overload_flush_states,
                 state_search,
                 state_insert,
                 state_remove,
                 source_search,
                 source_insert,
                 source_remove,
                 packets_in,
                 packets_in_blocked,
                 packets_in_scrubbed,
                 packets_v6_in,
                 packets_v6_in_blocked,
                 pacjets_v6_in_scrubbed,
                 packets_out,
                 packets_out_blocked,
                 packets_out_scrubbed,
                 packets_v6_out,
                 packets_v6_out_blocked,
                 packets_v6_out_scrubbed,
                 bytes_in,
                 bytes_out,
                 bytes_v6_in,
                 bytes_v6_out,
                 stateid,
                 status,
                 state_current,
                 source_current,
                 since,
                 loglevel,
                 hostid,
                 reass,
                 iface,
                 pf_checksum):
        self.__dict__.update(locals())
        del self.self
                 
    def dump(self):
        for attr in self.__dict__.iteritems():
            print "%s = %s" % attr

    def get_wanted_metrics(self):
        """Overrides MetricCollectorMixin.get_wanted_metrics()"""
        return {
            'states.current': 'state_current',
            'states.searches': 'state_search',
            'states.inserts': 'state_insert',
            'states.removes': 'state_remove',
            'bytes.out': 'bytes_out',
            'bytes.in': 'bytes_in',
            'packets.in.blocked': 'packets_in_blocked',
            'packets.in.passed': 'packets_in',
            'packets.out.blocked': 'packets_out_blocked',
            'packets.out.passed': 'packets_out',
            }
        
