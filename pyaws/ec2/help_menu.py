"""

Help Menu
    Help menu object containing body of help content.
    For printing with formatting

"""

from pyaws.core.colors import Colors

PACKAGE = 'machineimage'
PKG_ACCENT = Colors.ORANGE
PARAM_ACCENT = Colors.WHITE


synopsis_cmd = (
    Colors.RESET + PKG_ACCENT + PACKAGE +
    PARAM_ACCENT + '--image ' + Colors.RESET + '{OS_TYPE}' +
    PARAM_ACCENT + ' --profile ' + Colors.RESET + ' [PROFILE] ' +
    PARAM_ACCENT + ' --region ' + Colors.RESET + ' [REGION] '
    )

url_doc = Colors.URL + 'http://pyaws.readthedocs.io' + Colors.RESET
url_sc = Colors.URL + 'https://bitbucket.org/blakeca00/keyup' + Colors.RESET

menu_body = Colors.BOLD + """
  DESCRIPTION""" + Colors.RESET + """
            Automated Access Key Rotation for Amazon Web Services

            Official Docs:  """ + url_doc + """
            Source Code:  """ + url_sc + """
    """ + Colors.BOLD + """
  SYNOPSIS""" + Colors.RESET + """
                """ + synopsis_cmd + """

                    -i, --image    <value>
                    -p, --profile  <value>
                   [-d, --details  ]
                   [-f, --format    <value> ]
                   [-n, --filename  <value> ]
                   [-d, --debug    ]
                   [-h, --help     ]
                   [-V, --version  ]
    """ + Colors.BOLD + """
  OPTIONS
    """ + Colors.BOLD + """
        -i, --image""" + Colors.RESET + """ (string) : Amazon Machine Image Operating System type.
            Must be value from the following list.

                Valid EC2 Amazon Machine Image (AMI) Values:

                    - amazonlinux1       : Amazon Linux v1 (2018)
                    - amazonlinux2       : Amazon Linux v2 (2017.12+)
                    - redhat7.5          : Redhat Enterprise Linux 7.5
                    - redhat7.4          : Redhat Enterprise Linux 7.4
                    - redhat7.3          : Redhat Enterprise Linux 7.3
                    - ubuntu14.04        : Ubuntu Linux 14.04
                    - ubuntu16.04        : Ubuntu Linux 16.04
                    - ubuntu18.04        : Ubuntu Linux 18.04

                    Default: """ + Colors.BOLD + 'list' + Colors.RESET + """
    """ + Colors.BOLD + """
        -p, --profile""" + Colors.RESET + """ (string) : Profile name of an IAM user from the local
            awscli config for which you want to rotate access keys
    """ + Colors.BOLD + """
        -a, --auto""" + Colors.RESET + """ : Suppress output to stdout when """ + PACKAGE + """ triggered via a sched-
            uler such as cron or by some other automated means to rotate keys
            on a periodic schedule.
    """ + Colors.BOLD + """
        -c, --configure""" + Colors.RESET + """ :  Configure parameters to custom values. If the local
            config file does not exist, option writes a new local configuration
    """ + Colors.BOLD + """
        -d, --debug""" + Colors.RESET + """ : when True, do not write to the local awscli configuration
            file(s). Instead, write to a temporary location for testing the int-
            grity of the credentials file format that is written to disk.
    """ + Colors.BOLD + """
        -V, --version""" + Colors.RESET + """ : Print package version
    """ + Colors.BOLD + """
        -h, --help""" + Colors.RESET + """ : Show this help message and exit

    """
