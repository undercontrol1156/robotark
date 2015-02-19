var CATEGORIES = {
    'mechanics': {
        'general': 'general',
        'pneumatics': [
            'theory',
            'datasheets'
        ],
        'gearbox': 'gearbox',
        'drivetrain': 'drivetrain',
        'design': 'design'
    },
    'electronics': {
        'datasheets': [
            'components',
            'cots'
        ],
        'wiring': 'wiring',
        'controlsystem': [
            'crio',
            'roborio',
            'arduino',
            'others'
        ],
        'sensoring': 'sensoring',
        'theory': [
            'begginers',
            'advanced'
        ]
    },
    'programming': {
        'c': [
            'general',
            'windriver',
            'sensoring'
        ],
        'labview': [
            'basics',
            'cv',
            'signalanalysis',
            'sensoring'
        ],
        'java': [
            'general',
            'eclipse',
            'examples',
            'fullsystem'
        ],
        'examples': 'examples'
    },
    'cad': {
        'autocad': 'autocad',
        'inventor': 'inventor',
        'solidworks': 'solidworks',
        'models': [
            'robots',
            'gearbox',
            'drivetrain',
            'others'
        ],
        'others': 'others'
    },
    'team': [
        'scouting',
        'sponsors',
        'chairmans',
        'events',
        'websites'
    ]
};


function setOptions(chosen) {
    'use strict';
    var selbox = document.uploadForm.subcategory;
    selbox.options.length = 0;
    if (chosen === "electronics") {
        selbox.options[selbox.options.length] = new Option('Wiring', '/electronics/wiring');
        selbox.options[selbox.options.length] = new Option('Datasheets', '/electronics/datasheets');
        selbox.options[selbox.options.length] = new Option('Control System', '/electronics/controlsystem');
        selbox.options[selbox.options.length] = new Option('Sensoring', '/electronics/sensoring');
        selbox.options[selbox.options.length] = new Option('Theory', '/electronics/theory');
    }
    if (chosen === "programming") {
        selbox.options[selbox.options.length] = new Option('C', '/programming/c');
        selbox.options[selbox.options.length] = new Option('LabVIEW', '/programming/labview');
        selbox.options[selbox.options.length] = new Option('Java', '/programming/java');
    }
    if (chosen === "mechanics") {
        selbox.options[selbox.options.length] = new Option('General', '/mechanics/general');
        selbox.options[selbox.options.length] = new Option('Design', '/mechanics/design');
        selbox.options[selbox.options.length] = new Option('Pneumatics', '/mechanics/pneumatics');
        selbox.options[selbox.options.length] = new Option('Gear Box', '/mechanics/gearbox');
        selbox.options[selbox.options.length] = new Option('Drivetrain', '/mechanics/drivetrain');
    }
    if (chosen === "cad") {
        selbox.options[selbox.options.length] = new Option('Inventor', '/cad/inventor');
        selbox.options[selbox.options.length] = new Option('AutoCAD', '/cad/autocad');
        selbox.options[selbox.options.length] = new Option('SolidWorks', '/cad/solidworks');
        selbox.options[selbox.options.length] = new Option('Models', '/cad/models');
        selbox.options[selbox.options.length] = new Option('Others', '/cad/others');
    }
    if (chosen === "team") {
        selbox.options[selbox.options.length] = new Option('Events', '/team/events');
        selbox.options[selbox.options.length] = new Option('Scouting', '/team/scouting');
        selbox.options[selbox.options.length] = new Option('Sponsors', '/team/sponsors');
        selbox.options[selbox.options.length] = new Option('Websites', '/team/websites');
        selbox.options[selbox.options.length] = new Option('Chairmans', '/team/chairmans');
        selbox.options[selbox.options.length] = new Option('Safety', '/team/safety');
        selbox.options[selbox.options.length] = new Option('------', '/team');
    }
}
function setOptions2(chosen) {
    'use strict';
    var selbox = document.uploadForm.subsubcategory;
    selbox.options.length = 0;
    if (chosen === "/electronics/controlsystem") {
        selbox.options[selbox.options.length] = new Option('cRIO', '/electronics/controlsystem/crio');
        selbox.options[selbox.options.length] = new Option('RoboRIO', '/electronics/controlsystem/roborio');
        selbox.options[selbox.options.length] = new Option('Arduino', '/electronics/controlsystem/arduino');
        selbox.options[selbox.options.length] = new Option('Others', '/electronics/controlsystem/others');
    }
    if (chosen === "/electronics/datasheets") {
        selbox.options[selbox.options.length] = new Option('Sensors', '/electronics/datasheets/sensors');
        selbox.options[selbox.options.length] = new Option('Components', '/electronics/datasheets/components');
        selbox.options[selbox.options.length] = new Option('COTS', '/electronics/datasheets/cots');
    }
    if (chosen === "/electronics/theory") {
        selbox.options[selbox.options.length] = new Option('Begginers', '/electronics/theory/begginers');
        selbox.options[selbox.options.length] = new Option('Advanced', '/electronics/theory/advanced');
    }
    if (chosen === "/mechanics/pneumatics") {
        selbox.options[selbox.options.length] = new Option('Theory', '/mechanics/pneumatics/theory');
        selbox.options[selbox.options.length] = new Option('Datasheets', '/mechanics/pneumatics/datasheets');
    }
    if (chosen === "/programming/c") {
        selbox.options[selbox.options.length] = new Option('General', '/programming/c/general');
        selbox.options[selbox.options.length] = new Option('WindRiver', '/programming/c/windriver');
        selbox.options[selbox.options.length] = new Option('Sensoring', '/programming/c/sensoring');
        selbox.options[selbox.options.length] = new Option('Examples', '/programming/c/examples');
        selbox.options[selbox.options.length] = new Option('Full System', '/programming/c/fullsystem');
    }
    if (chosen === "/programming/java") {
        selbox.options[selbox.options.length] = new Option('General', '/programming/java/general');
        selbox.options[selbox.options.length] = new Option('Eclipse', '/programming/java/eclipse');
        selbox.options[selbox.options.length] = new Option('Examples', '/programming/java/examples');
        selbox.options[selbox.options.length] = new Option('Full System', '/programming/java/fullsystem');
    }
    if (chosen === "/programming/labview") {
        selbox.options[selbox.options.length] = new Option('Basics', '/programming/labview/basics');
        selbox.options[selbox.options.length] = new Option('Computer Vision', '/programming/labview/cv');
        selbox.options[selbox.options.length] = new Option('Sensoring', '/programming/labview/sensoring');
        selbox.options[selbox.options.length] = new Option('Signal Analysis', '/programming/labview/signalanalysis');
        selbox.options[selbox.options.length] = new Option('Examples', '/programming/labview/examples');
        selbox.options[selbox.options.length] = new Option('Full System', '/programming/labview/fullsystem');
    }
    if (chosen === "/cad/models") {
        selbox.options[selbox.options.length] = new Option('Robots', '/cad/models/robots');
        selbox.options[selbox.options.length] = new Option('Gearbox', '/cad/models/gearbox');
        selbox.options[selbox.options.length] = new Option('Drivetrain', '/cad/models/drivetrain');
        selbox.options[selbox.options.length] = new Option('Others', '/cad/models/others');
    }
    else {
        selbox.options[selbox.options.length] = new Option('------', chosen);
    }
}
