import copy
from prediction_engine import prediction_engine
from data_loader import weather_loader

# Comprehensive Indian Railways Pan-India Fleet Dataset
# Covers Vande Bharat, Rajdhani, Shatabdi, Duronto, Tejas, Superfast Mail & Humsafar trains across all Indian Railway zones.
MOCK_TRAINS = [
    # --- 1. VANDE BHARAT EXPRESSES ---
    {
        "id": "22436",
        "number": "22436",
        "name": "New Delhi - Varanasi Vande Bharat Express",
        "type": "Vande Bharat",
        "priority": 1,
        "max_speed": 160.0,
        "origin": "New Delhi (NDLS)",
        "destination": "Varanasi Junction (BSB)",
        "current_station": "Kanpur Central (CNB)",
        "next_station": "Prayagraj Junction (PRYJ)",
        "lat": 26.4499,
        "lon": 80.3319,
        "progress_pct": 58.0,
        "remaining_distance_km": 318.0,
        "section_occupancy": "GREEN",
        "route_junctions": [
            {"name": "New Delhi", "code": "NDLS", "km": 0, "lat": 28.6139, "lon": 77.2090, "arr": "06:00", "dep": "06:00"},
            {"name": "Kanpur Central", "code": "CNB", "km": 440, "lat": 26.4499, "lon": 80.3319, "arr": "10:08", "dep": "10:10"},
            {"name": "Prayagraj Junction", "code": "PRYJ", "km": 634, "lat": 25.4358, "lon": 81.8463, "arr": "12:08", "dep": "12:10"},
            {"name": "Varanasi Junction", "code": "BSB", "km": 758, "lat": 25.3176, "lon": 82.9739, "arr": "14:00", "dep": "14:00"}
        ]
    },
    {
        "id": "20901",
        "number": "20901",
        "name": "Mumbai - Gandhinagar Vande Bharat Express",
        "type": "Vande Bharat",
        "priority": 1,
        "max_speed": 160.0,
        "origin": "Mumbai Central (MMCT)",
        "destination": "Gandhinagar Capital (GNC)",
        "current_station": "Surat (ST)",
        "next_station": "Vadodara Junction (BRC)",
        "lat": 21.1702,
        "lon": 72.8311,
        "progress_pct": 51.0,
        "remaining_distance_km": 257.0,
        "section_occupancy": "GREEN",
        "route_junctions": [
            {"name": "Mumbai Central", "code": "MMCT", "km": 0, "lat": 18.9696, "lon": 72.8193, "arr": "06:00", "dep": "06:00"},
            {"name": "Borivali", "code": "BVI", "km": 30, "lat": 19.2291, "lon": 72.8573, "arr": "06:23", "dep": "06:25"},
            {"name": "Vapi", "code": "VAPI", "km": 168, "lat": 20.3720, "lon": 72.9030, "arr": "08:00", "dep": "08:02"},
            {"name": "Surat", "code": "ST", "km": 263, "lat": 21.1702, "lon": 72.8311, "arr": "08:58", "dep": "09:03"},
            {"name": "Vadodara Junction", "code": "BRC", "km": 393, "lat": 22.3072, "lon": 73.1812, "arr": "10:13", "dep": "10:16"},
            {"name": "Ahmedabad Junction", "code": "ADI", "km": 493, "lat": 23.0225, "lon": 72.5714, "arr": "11:25", "dep": "11:30"},
            {"name": "Gandhinagar Capital", "code": "GNC", "km": 520, "lat": 23.2300, "lon": 72.6300, "arr": "12:25", "dep": "12:25"}
        ]
    },
    {
        "id": "20607",
        "number": "20607",
        "name": "Chennai - Mysuru Vande Bharat Express",
        "type": "Vande Bharat",
        "priority": 1,
        "max_speed": 160.0,
        "origin": "MGR Chennai Central (MAS)",
        "destination": "Mysuru Junction (MYS)",
        "current_station": "Katpadi Junction (KPD)",
        "next_station": "KSR Bengaluru (SBC)",
        "lat": 12.9698,
        "lon": 79.1350,
        "progress_pct": 27.0,
        "remaining_distance_km": 365.0,
        "section_occupancy": "GREEN",
        "route_junctions": [
            {"name": "Chennai Central", "code": "MAS", "km": 0, "lat": 13.0827, "lon": 80.2707, "arr": "05:50", "dep": "05:50"},
            {"name": "Katpadi Junction", "code": "KPD", "km": 130, "lat": 12.9698, "lon": 79.1350, "arr": "07:13", "dep": "07:15"},
            {"name": "KSR Bengaluru", "code": "SBC", "km": 359, "lat": 12.9716, "lon": 77.5946, "arr": "10:15", "dep": "10:20"},
            {"name": "Mysuru Junction", "code": "MYS", "km": 496, "lat": 12.3168, "lon": 76.6433, "arr": "12:20", "dep": "12:20"}
        ]
    },
    {
        "id": "22895",
        "number": "22895",
        "name": "Howrah - Puri Vande Bharat Express",
        "type": "Vande Bharat",
        "priority": 1,
        "max_speed": 160.0,
        "origin": "Howrah Junction (HWH)",
        "destination": "Puri (PURI)",
        "current_station": "Kharagpur Junction (KGP)",
        "next_station": "Balasore (BLS)",
        "lat": 22.3392,
        "lon": 87.3243,
        "progress_pct": 23.0,
        "remaining_distance_km": 387.0,
        "section_occupancy": "GREEN",
        "route_junctions": [
            {"name": "Howrah Junction", "code": "HWH", "km": 0, "lat": 22.5858, "lon": 88.3426, "arr": "06:10", "dep": "06:10"},
            {"name": "Kharagpur Junction", "code": "KGP", "km": 115, "lat": 22.3392, "lon": 87.3243, "arr": "07:40", "dep": "07:42"},
            {"name": "Balasore", "code": "BLS", "km": 231, "lat": 21.4934, "lon": 86.9135, "arr": "09:03", "dep": "09:05"},
            {"name": "Bhadrak", "code": "BHC", "km": 293, "lat": 21.0543, "lon": 86.5186, "arr": "09:40", "dep": "09:42"},
            {"name": "Cuttack Junction", "code": "CTC", "km": 409, "lat": 20.4625, "lon": 85.8828, "arr": "10:50", "dep": "10:52"},
            {"name": "Bhubaneswar", "code": "BBS", "km": 437, "lat": 20.2961, "lon": 85.8245, "arr": "11:20", "dep": "11:24"},
            {"name": "Puri", "code": "PURI", "km": 502, "lat": 19.8135, "lon": 85.8312, "arr": "12:35", "dep": "12:35"}
        ]
    },
    {
        "id": "22439",
        "number": "22439",
        "name": "New Delhi - Katra Vande Bharat Express",
        "type": "Vande Bharat",
        "priority": 1,
        "max_speed": 160.0,
        "origin": "New Delhi (NDLS)",
        "destination": "Shri Mata Vaishno Devi Katra (SVDK)",
        "current_station": "Ludhiana Junction (LDH)",
        "next_station": "Jammu Tawi (JAT)",
        "lat": 30.9010,
        "lon": 75.8573,
        "progress_pct": 48.0,
        "remaining_distance_km": 340.0,
        "section_occupancy": "GREEN",
        "route_junctions": [
            {"name": "New Delhi", "code": "NDLS", "km": 0, "lat": 28.6139, "lon": 77.2090, "arr": "06:00", "dep": "06:00"},
            {"name": "Ambala Cantt", "code": "UMB", "km": 198, "lat": 30.3752, "lon": 76.7821, "arr": "08:10", "dep": "08:12"},
            {"name": "Ludhiana Junction", "code": "LDH", "km": 312, "lat": 30.9010, "lon": 75.8573, "arr": "09:19", "dep": "09:21"},
            {"name": "Jammu Tawi", "code": "JAT", "km": 577, "lat": 32.7266, "lon": 74.8570, "arr": "12:38", "dep": "12:40"},
            {"name": "Shri Mata Vaishno Devi Katra", "code": "SVDK", "km": 655, "lat": 32.9904, "lon": 74.9317, "arr": "14:00", "dep": "14:00"}
        ]
    },
    {
        "id": "20701",
        "number": "20701",
        "name": "Secunderabad - Tirupati Vande Bharat Express",
        "type": "Vande Bharat",
        "priority": 1,
        "max_speed": 160.0,
        "origin": "Secunderabad (SC)",
        "destination": "Tirupati (TPTY)",
        "current_station": "Guntur Junction (GNT)",
        "next_station": "Ongole (OGL)",
        "lat": 16.3067,
        "lon": 80.4365,
        "progress_pct": 43.0,
        "remaining_distance_km": 375.0,
        "section_occupancy": "GREEN",
        "route_junctions": [
            {"name": "Secunderabad", "code": "SC", "km": 0, "lat": 17.4399, "lon": 78.5017, "arr": "06:15", "dep": "06:15"},
            {"name": "Nalgonda", "code": "NLDA", "km": 110, "lat": 17.0500, "lon": 79.2700, "arr": "07:29", "dep": "07:30"},
            {"name": "Guntur Junction", "code": "GNT", "km": 281, "lat": 16.3067, "lon": 80.4365, "arr": "09:30", "dep": "09:35"},
            {"name": "Ongole", "code": "OGL", "km": 418, "lat": 15.5057, "lon": 80.0499, "arr": "11:03", "dep": "11:05"},
            {"name": "Nellore", "code": "NLR", "km": 535, "lat": 14.4426, "lon": 79.9865, "arr": "12:13", "dep": "12:15"},
            {"name": "Tirupati", "code": "TPTY", "km": 661, "lat": 13.6288, "lon": 79.4192, "arr": "14:30", "dep": "14:30"}
        ]
    },

    # --- 2. RAJDHANI EXPRESSES ---
    {
        "id": "12951",
        "number": "12951",
        "name": "Mumbai Rajdhani Express",
        "type": "Superfast Rajdhani",
        "priority": 1,
        "max_speed": 130.0,
        "origin": "New Delhi (NDLS)",
        "destination": "Mumbai Central (MMCT)",
        "current_station": "Agra Cantt (AGC)",
        "next_station": "Gwalior Junction (GWL)",
        "lat": 27.1577,
        "lon": 78.0076,
        "progress_pct": 32.5,
        "remaining_distance_km": 1120.0,
        "section_occupancy": "GREEN",
        "route_junctions": [
            {"name": "New Delhi", "code": "NDLS", "km": 0, "lat": 28.6139, "lon": 77.2090, "arr": "16:55", "dep": "16:55"},
            {"name": "Agra Cantt", "code": "AGC", "km": 195, "lat": 27.1577, "lon": 78.0076, "arr": "18:42", "dep": "18:45"},
            {"name": "Gwalior Junction", "code": "GWL", "km": 313, "lat": 26.2183, "lon": 78.1828, "arr": "20:05", "dep": "20:07"},
            {"name": "VGL Jhansi", "code": "VGLJ", "km": 411, "lat": 25.4484, "lon": 78.5685, "arr": "21:28", "dep": "21:33"},
            {"name": "Bhopal Junction", "code": "BPL", "km": 703, "lat": 23.2599, "lon": 77.4126, "arr": "01:30", "dep": "01:40"},
            {"name": "Ratlam Junction", "code": "RTM", "km": 1092, "lat": 23.3315, "lon": 75.0367, "arr": "06:40", "dep": "06:45"},
            {"name": "Surat", "code": "ST", "km": 1298, "lat": 21.1702, "lon": 72.8311, "arr": "09:42", "dep": "09:47"},
            {"name": "Mumbai Central", "code": "MMCT", "km": 1384, "lat": 18.9696, "lon": 72.8193, "arr": "11:35", "dep": "11:35"}
        ]
    },
    {
        "id": "12301",
        "number": "12301",
        "name": "Howrah Rajdhani Express (via Gaya)",
        "type": "Superfast Rajdhani",
        "priority": 1,
        "max_speed": 130.0,
        "origin": "Howrah Junction (HWH)",
        "destination": "New Delhi (NDLS)",
        "current_station": "Gaya Junction (GAYA)",
        "next_station": "Pt. Deen Dayal Upadhyaya (DDU)",
        "lat": 24.7955,
        "lon": 85.0002,
        "progress_pct": 32.0,
        "remaining_distance_km": 985.0,
        "section_occupancy": "GREEN",
        "route_junctions": [
            {"name": "Howrah Junction", "code": "HWH", "km": 0, "lat": 22.5858, "lon": 88.3426, "arr": "16:50", "dep": "16:50"},
            {"name": "Asansol Junction", "code": "ASN", "km": 200, "lat": 23.6889, "lon": 86.9661, "arr": "19:00", "dep": "19:03"},
            {"name": "Dhanbad Junction", "code": "DHN", "km": 259, "lat": 23.7957, "lon": 86.4304, "arr": "19:55", "dep": "20:00"},
            {"name": "Gaya Junction", "code": "GAYA", "km": 458, "lat": 24.7955, "lon": 85.0002, "arr": "22:19", "dep": "22:22"},
            {"name": "Pt. DD Upadhyaya", "code": "DDU", "km": 663, "lat": 25.2816, "lon": 83.1189, "arr": "00:45", "dep": "00:55"},
            {"name": "Prayagraj Junction", "code": "PRYJ", "km": 816, "lat": 25.4358, "lon": 81.8463, "arr": "02:43", "dep": "02:45"},
            {"name": "Kanpur Central", "code": "CNB", "km": 1010, "lat": 26.4499, "lon": 80.3319, "arr": "04:40", "dep": "04:45"},
            {"name": "New Delhi", "code": "NDLS", "km": 1451, "lat": 28.6139, "lon": 77.2090, "arr": "10:05", "dep": "10:05"}
        ]
    },
    {
        "id": "22691",
        "number": "22691",
        "name": "Bengaluru Rajdhani Express",
        "type": "Superfast Rajdhani",
        "priority": 1,
        "max_speed": 130.0,
        "origin": "KSR Bengaluru (SBC)",
        "destination": "Hazrat Nizamuddin (NZM)",
        "current_station": "Secunderabad (SC)",
        "next_station": "Nagpur Junction (NGP)",
        "lat": 17.4399,
        "lon": 78.5017,
        "progress_pct": 27.0,
        "remaining_distance_km": 1715.0,
        "section_occupancy": "YELLOW",
        "route_junctions": [
            {"name": "KSR Bengaluru", "code": "SBC", "km": 0, "lat": 12.9716, "lon": 77.5946, "arr": "20:00", "dep": "20:00"},
            {"name": "Anantapur", "code": "ATP", "km": 215, "lat": 14.6819, "lon": 77.6006, "arr": "23:08", "dep": "23:10"},
            {"name": "Secunderabad", "code": "SC", "km": 637, "lat": 17.4399, "lon": 78.5017, "arr": "07:05", "dep": "07:15"},
            {"name": "Nagpur Junction", "code": "NGP", "km": 1218, "lat": 21.1458, "lon": 79.0882, "arr": "15:20", "dep": "15:25"},
            {"name": "Bhopal Junction", "code": "BPL", "km": 1608, "lat": 23.2599, "lon": 77.4126, "arr": "20:55", "dep": "21:05"},
            {"name": "VGL Jhansi", "code": "VGLJ", "km": 1900, "lat": 25.4484, "lon": 78.5685, "arr": "00:26", "dep": "00:31"},
            {"name": "Gwalior Junction", "code": "GWL", "km": 1998, "lat": 26.2183, "lon": 78.1828, "arr": "01:30", "dep": "01:32"},
            {"name": "Agra Cantt", "code": "AGC", "km": 2116, "lat": 27.1577, "lon": 78.0076, "arr": "02:50", "dep": "02:52"},
            {"name": "Hazrat Nizamuddin", "code": "NZM", "km": 2352, "lat": 28.5888, "lon": 77.2534, "arr": "05:30", "dep": "05:30"}
        ]
    },
    {
        "id": "12433",
        "number": "12433",
        "name": "Chennai Rajdhani Express",
        "type": "Superfast Rajdhani",
        "priority": 1,
        "max_speed": 130.0,
        "origin": "MGR Chennai Central (MAS)",
        "destination": "Hazrat Nizamuddin (NZM)",
        "current_station": "Vijayawada Junction (BZA)",
        "next_station": "Warangal (WL)",
        "lat": 16.5062,
        "lon": 80.6480,
        "progress_pct": 20.0,
        "remaining_distance_km": 1740.0,
        "section_occupancy": "GREEN",
        "route_junctions": [
            {"name": "Chennai Central", "code": "MAS", "km": 0, "lat": 13.0827, "lon": 80.2707, "arr": "06:10", "dep": "06:10"},
            {"name": "Vijayawada Junction", "code": "BZA", "km": 431, "lat": 16.5062, "lon": 80.6480, "arr": "11:40", "dep": "11:50"},
            {"name": "Warangal", "code": "WL", "km": 638, "lat": 17.9689, "lon": 79.5941, "arr": "14:12", "dep": "14:14"},
            {"name": "Balharshah", "code": "BPQ", "km": 881, "lat": 19.8540, "lon": 79.3414, "arr": "17:40", "dep": "17:45"},
            {"name": "Nagpur Junction", "code": "NGP", "km": 1090, "lat": 21.1458, "lon": 79.0882, "arr": "20:25", "dep": "20:30"},
            {"name": "Bhopal Junction", "code": "BPL", "km": 1480, "lat": 23.2599, "lon": 77.4126, "arr": "02:00", "dep": "02:10"},
            {"name": "VGL Jhansi", "code": "VGLJ", "km": 1772, "lat": 25.4484, "lon": 78.5685, "arr": "05:20", "dep": "05:25"},
            {"name": "Agra Cantt", "code": "AGC", "km": 1988, "lat": 27.1577, "lon": 78.0076, "arr": "07:50", "dep": "07:52"},
            {"name": "Hazrat Nizamuddin", "code": "NZM", "km": 2176, "lat": 28.5888, "lon": 77.2534, "arr": "10:30", "dep": "10:30"}
        ]
    },
    {
        "id": "20503",
        "number": "20503",
        "name": "Dibrugarh Rajdhani Express",
        "type": "Superfast Rajdhani",
        "priority": 1,
        "max_speed": 130.0,
        "origin": "Dibrugarh (DBRG)",
        "destination": "New Delhi (NDLS)",
        "current_station": "Guwahati (GHY)",
        "next_station": "New Jalpaiguri (NJP)",
        "lat": 26.1863,
        "lon": 91.7490,
        "progress_pct": 23.0,
        "remaining_distance_km": 1890.0,
        "section_occupancy": "GREEN",
        "route_junctions": [
            {"name": "Dibrugarh", "code": "DBRG", "km": 0, "lat": 27.4728, "lon": 94.9120, "arr": "19:55", "dep": "19:55"},
            {"name": "Guwahati", "code": "GHY", "km": 560, "lat": 26.1863, "lon": 91.7490, "arr": "05:20", "dep": "05:35"},
            {"name": "New Jalpaiguri", "code": "NJP", "km": 985, "lat": 26.6858, "lon": 88.4416, "arr": "12:15", "dep": "12:25"},
            {"name": "Katihar Junction", "code": "KIR", "km": 1169, "lat": 25.5434, "lon": 87.5684, "arr": "15:05", "dep": "15:15"},
            {"name": "Barauni Junction", "code": "BJU", "km": 1348, "lat": 25.4744, "lon": 85.9723, "arr": "18:00", "dep": "18:10"},
            {"name": "Patliputra", "code": "PPTA", "km": 1456, "lat": 25.6200, "lon": 85.0800, "arr": "20:10", "dep": "20:20"},
            {"name": "Pt. DD Upadhyaya", "code": "DDU", "km": 1665, "lat": 25.2816, "lon": 83.1189, "arr": "22:50", "dep": "23:00"},
            {"name": "Kanpur Central", "code": "CNB", "km": 2012, "lat": 26.4499, "lon": 80.3319, "arr": "02:40", "dep": "02:45"},
            {"name": "New Delhi", "code": "NDLS", "km": 2452, "lat": 28.6139, "lon": 77.2090, "arr": "08:30", "dep": "08:30"}
        ]
    },
    {
        "id": "12309",
        "number": "12309",
        "name": "Patna Rajdhani Express",
        "type": "Superfast Rajdhani",
        "priority": 1,
        "max_speed": 130.0,
        "origin": "Rajendra Nagar Patna (RJPB)",
        "destination": "New Delhi (NDLS)",
        "current_station": "Pt. Deen Dayal Upadhyaya (DDU)",
        "next_station": "Prayagraj Junction (PRYJ)",
        "lat": 25.2816,
        "lon": 83.1189,
        "progress_pct": 22.0,
        "remaining_distance_km": 780.0,
        "section_occupancy": "GREEN",
        "route_junctions": [
            {"name": "Rajendra Nagar", "code": "RJPB", "km": 0, "lat": 25.5941, "lon": 85.1612, "arr": "19:10", "dep": "19:10"},
            {"name": "Patna Junction", "code": "PNBE", "km": 3, "lat": 25.6022, "lon": 85.1376, "arr": "19:25", "dep": "19:35"},
            {"name": "Pt. DD Upadhyaya", "code": "DDU", "km": 214, "lat": 25.2816, "lon": 83.1189, "arr": "22:12", "dep": "22:22"},
            {"name": "Prayagraj Junction", "code": "PRYJ", "km": 367, "lat": 25.4358, "lon": 81.8463, "arr": "00:10", "dep": "00:12"},
            {"name": "Kanpur Central", "code": "CNB", "km": 561, "lat": 26.4499, "lon": 80.3319, "arr": "02:15", "dep": "02:20"},
            {"name": "New Delhi", "code": "NDLS", "km": 1002, "lat": 28.6139, "lon": 77.2090, "arr": "07:40", "dep": "07:40"}
        ]
    },
    {
        "id": "12431",
        "number": "12431",
        "name": "Trivandrum Rajdhani Express (via Konkan)",
        "type": "Superfast Rajdhani",
        "priority": 1,
        "max_speed": 130.0,
        "origin": "Thiruvananthapuram (TVC)",
        "destination": "Hazrat Nizamuddin (NZM)",
        "current_station": "Madgaon Junction (MAO)",
        "next_station": "Panvel (PNVL)",
        "lat": 15.2736,
        "lon": 73.9580,
        "progress_pct": 39.0,
        "remaining_distance_km": 1910.0,
        "section_occupancy": "GREEN",
        "route_junctions": [
            {"name": "Thiruvananthapuram", "code": "TVC", "km": 0, "lat": 8.4875, "lon": 76.9525, "arr": "19:15", "dep": "19:15"},
            {"name": "Ernakulam Junction", "code": "ERS", "km": 206, "lat": 9.9674, "lon": 76.2917, "arr": "22:30", "dep": "22:35"},
            {"name": "Kozhikode", "code": "CLT", "km": 399, "lat": 11.2480, "lon": 75.7839, "arr": "01:17", "dep": "01:20"},
            {"name": "Mangaluru Junction", "code": "MAJN", "km": 621, "lat": 12.8703, "lon": 74.8806, "arr": "04:45", "dep": "04:50"},
            {"name": "Madgaon Junction", "code": "MAO", "km": 935, "lat": 15.2736, "lon": 73.9580, "arr": "09:50", "dep": "10:00"},
            {"name": "Panvel", "code": "PNVL", "km": 1475, "lat": 18.9902, "lon": 73.1168, "arr": "18:00", "dep": "18:05"},
            {"name": "Surat", "code": "ST", "km": 1762, "lat": 21.1702, "lon": 72.8311, "arr": "22:15", "dep": "22:18"},
            {"name": "Vadodara Junction", "code": "BRC", "km": 1892, "lat": 22.3072, "lon": 73.1812, "arr": "23:48", "dep": "23:58"},
            {"name": "Kota Junction", "code": "KOTA", "km": 2420, "lat": 25.2138, "lon": 75.8648, "arr": "06:15", "dep": "06:25"},
            {"name": "Hazrat Nizamuddin", "code": "NZM", "km": 2848, "lat": 28.5888, "lon": 77.2534, "arr": "12:30", "dep": "12:30"}
        ]
    },

    # --- 3. SHATABDI & TEJAS EXPRESSES ---
    {
        "id": "12002",
        "number": "12002",
        "name": "Bhopal Shatabdi Express",
        "type": "Shatabdi",
        "priority": 1,
        "max_speed": 150.0,
        "origin": "New Delhi (NDLS)",
        "destination": "Rani Kamlapati (RKMP)",
        "current_station": "Mathura Junction (MTJ)",
        "next_station": "Agra Cantt (AGC)",
        "lat": 27.4924,
        "lon": 77.6737,
        "progress_pct": 20.0,
        "remaining_distance_km": 560.0,
        "section_occupancy": "GREEN",
        "route_junctions": [
            {"name": "New Delhi", "code": "NDLS", "km": 0, "lat": 28.6139, "lon": 77.2090, "arr": "06:00", "dep": "06:00"},
            {"name": "Mathura Junction", "code": "MTJ", "km": 141, "lat": 27.4924, "lon": 77.6737, "arr": "07:19", "dep": "07:20"},
            {"name": "Agra Cantt", "code": "AGC", "km": 195, "lat": 27.1577, "lon": 78.0076, "arr": "07:50", "dep": "07:55"},
            {"name": "Gwalior Junction", "code": "GWL", "km": 313, "lat": 26.2183, "lon": 78.1828, "arr": "09:23", "dep": "09:28"},
            {"name": "VGL Jhansi", "code": "VGLJ", "km": 411, "lat": 25.4484, "lon": 78.5685, "arr": "10:45", "dep": "10:50"},
            {"name": "Bhopal Junction", "code": "BPL", "km": 703, "lat": 23.2599, "lon": 77.4126, "arr": "14:07", "dep": "14:12"},
            {"name": "Rani Kamlapati", "code": "RKMP", "km": 709, "lat": 23.2200, "lon": 77.4400, "arr": "14:40", "dep": "14:40"}
        ]
    },
    {
        "id": "12009",
        "number": "12009",
        "name": "Mumbai - Ahmedabad Shatabdi Express",
        "type": "Shatabdi",
        "priority": 1,
        "max_speed": 130.0,
        "origin": "Mumbai Central (MMCT)",
        "destination": "Ahmedabad Junction (ADI)",
        "current_station": "Surat (ST)",
        "next_station": "Vadodara Junction (BRC)",
        "lat": 21.1702,
        "lon": 72.8311,
        "progress_pct": 54.0,
        "remaining_distance_km": 230.0,
        "section_occupancy": "YELLOW",
        "route_junctions": [
            {"name": "Mumbai Central", "code": "MMCT", "km": 0, "lat": 18.9696, "lon": 72.8193, "arr": "06:20", "dep": "06:20"},
            {"name": "Borivali", "code": "BVI", "km": 30, "lat": 19.2291, "lon": 72.8573, "arr": "06:48", "dep": "06:50"},
            {"name": "Vapi", "code": "VAPI", "km": 168, "lat": 20.3720, "lon": 72.9030, "arr": "08:24", "dep": "08:26"},
            {"name": "Surat", "code": "ST", "km": 263, "lat": 21.1702, "lon": 72.8311, "arr": "09:45", "dep": "09:50"},
            {"name": "Vadodara Junction", "code": "BRC", "km": 393, "lat": 22.3072, "lon": 73.1812, "arr": "11:30", "dep": "11:35"},
            {"name": "Ahmedabad Junction", "code": "ADI", "km": 493, "lat": 23.0225, "lon": 72.5714, "arr": "12:55", "dep": "12:55"}
        ]
    },
    {
        "id": "12013",
        "number": "12013",
        "name": "New Delhi - Amritsar Shatabdi Express",
        "type": "Shatabdi",
        "priority": 1,
        "max_speed": 130.0,
        "origin": "New Delhi (NDLS)",
        "destination": "Amritsar Junction (ASR)",
        "current_station": "Ambala Cantt (UMB)",
        "next_station": "Ludhiana Junction (LDH)",
        "lat": 30.3752,
        "lon": 76.7821,
        "progress_pct": 44.0,
        "remaining_distance_km": 250.0,
        "section_occupancy": "GREEN",
        "route_junctions": [
            {"name": "New Delhi", "code": "NDLS", "km": 0, "lat": 28.6139, "lon": 77.2090, "arr": "16:30", "dep": "16:30"},
            {"name": "Panipat Junction", "code": "PNP", "km": 89, "lat": 29.3909, "lon": 76.9635, "arr": "17:36", "dep": "17:38"},
            {"name": "Ambala Cantt", "code": "UMB", "km": 198, "lat": 30.3752, "lon": 76.7821, "arr": "18:51", "dep": "18:53"},
            {"name": "Ludhiana Junction", "code": "LDH", "km": 312, "lat": 30.9010, "lon": 75.8573, "arr": "20:16", "dep": "20:19"},
            {"name": "Jalandhar City", "code": "JUC", "km": 369, "lat": 31.3260, "lon": 75.5762, "arr": "21:14", "dep": "21:16"},
            {"name": "Amritsar Junction", "code": "ASR", "km": 448, "lat": 31.6340, "lon": 74.8723, "arr": "22:45", "dep": "22:45"}
        ]
    },
    {
        "id": "82901",
        "number": "82901",
        "name": "Mumbai - Ahmedabad Tejas Express",
        "type": "Tejas Express",
        "priority": 1,
        "max_speed": 140.0,
        "origin": "Mumbai Central (MMCT)",
        "destination": "Ahmedabad Junction (ADI)",
        "current_station": "Vapi (VAPI)",
        "next_station": "Surat (ST)",
        "lat": 20.3720,
        "lon": 72.9030,
        "progress_pct": 34.0,
        "remaining_distance_km": 325.0,
        "section_occupancy": "GREEN",
        "route_junctions": [
            {"name": "Mumbai Central", "code": "MMCT", "km": 0, "lat": 18.9696, "lon": 72.8193, "arr": "15:45", "dep": "15:45"},
            {"name": "Borivali", "code": "BVI", "km": 30, "lat": 19.2291, "lon": 72.8573, "arr": "16:11", "dep": "16:13"},
            {"name": "Vapi", "code": "VAPI", "km": 168, "lat": 20.3720, "lon": 72.9030, "arr": "17:48", "dep": "17:50"},
            {"name": "Surat", "code": "ST", "km": 263, "lat": 21.1702, "lon": 72.8311, "arr": "19:00", "dep": "19:05"},
            {"name": "Vadodara Junction", "code": "BRC", "km": 393, "lat": 22.3072, "lon": 73.1812, "arr": "20:30", "dep": "20:35"},
            {"name": "Ahmedabad Junction", "code": "ADI", "km": 493, "lat": 23.0225, "lon": 72.5714, "arr": "22:05", "dep": "22:05"}
        ]
    },

    # --- 4. DURONTO EXPRESSES ---
    {
        "id": "12261",
        "number": "12261",
        "name": "Howrah Duronto Express",
        "type": "Duronto",
        "priority": 1,
        "max_speed": 120.0,
        "origin": "CSMT Mumbai (CSMT)",
        "destination": "Howrah Junction (HWH)",
        "current_station": "Nagpur Junction (NGP)",
        "next_station": "Raipur Junction (R)",
        "lat": 21.1458,
        "lon": 79.0882,
        "progress_pct": 42.0,
        "remaining_distance_km": 1130.0,
        "section_occupancy": "GREEN",
        "route_junctions": [
            {"name": "CSMT Mumbai", "code": "CSMT", "km": 0, "lat": 18.9400, "lon": 72.8353, "arr": "17:15", "dep": "17:15"},
            {"name": "Igatpuri", "code": "IGP", "km": 137, "lat": 19.6953, "lon": 73.5606, "arr": "19:40", "dep": "19:45"},
            {"name": "Bhusaval Junction", "code": "BSL", "km": 445, "lat": 21.0454, "lon": 75.7891, "arr": "23:55", "dep": "00:00"},
            {"name": "Nagpur Junction", "code": "NGP", "km": 837, "lat": 21.1458, "lon": 79.0882, "arr": "05:40", "dep": "05:45"},
            {"name": "Raipur Junction", "code": "R", "km": 1139, "lat": 21.2514, "lon": 81.6296, "arr": "09:55", "dep": "10:00"},
            {"name": "Bilaspur Junction", "code": "BSP", "km": 1250, "lat": 22.0797, "lon": 82.1409, "arr": "11:45", "dep": "11:55"},
            {"name": "Rourkela Junction", "code": "ROU", "km": 1555, "lat": 22.2274, "lon": 84.8624, "arr": "15:45", "dep": "15:53"},
            {"name": "Tatanagar Junction", "code": "TATA", "km": 1718, "lat": 22.7699, "lon": 86.1884, "arr": "17:55", "dep": "18:05"},
            {"name": "Howrah Junction", "code": "HWH", "km": 1968, "lat": 22.5858, "lon": 88.3426, "arr": "20:15", "dep": "20:15"}
        ]
    },
    {
        "id": "12263",
        "number": "12263",
        "name": "Hazrat Nizamuddin - Pune Duronto Express",
        "type": "Duronto",
        "priority": 1,
        "max_speed": 120.0,
        "origin": "Hazrat Nizamuddin (NZM)",
        "destination": "Pune Junction (PUNE)",
        "current_station": "Kota Junction (KOTA)",
        "next_station": "Ratlam Junction (RTM)",
        "lat": 25.2138,
        "lon": 75.8648,
        "progress_pct": 31.0,
        "remaining_distance_km": 1050.0,
        "section_occupancy": "GREEN",
        "route_junctions": [
            {"name": "Hazrat Nizamuddin", "code": "NZM", "km": 0, "lat": 28.5888, "lon": 77.2534, "arr": "06:15", "dep": "06:15"},
            {"name": "Kota Junction", "code": "KOTA", "km": 458, "lat": 25.2138, "lon": 75.8648, "arr": "11:20", "dep": "11:30"},
            {"name": "Ratlam Junction", "code": "RTM", "km": 725, "lat": 23.3315, "lon": 75.0367, "arr": "15:00", "dep": "15:05"},
            {"name": "Vadodara Junction", "code": "BRC", "km": 985, "lat": 22.3072, "lon": 73.1812, "arr": "18:35", "dep": "18:45"},
            {"name": "Surat", "code": "ST", "km": 1115, "lat": 21.1702, "lon": 72.8311, "arr": "20:15", "dep": "20:20"},
            {"name": "Vasai Road", "code": "BSR", "km": 1331, "lat": 19.3812, "lon": 72.8314, "arr": "23:00", "dep": "23:05"},
            {"name": "Pune Junction", "code": "PUNE", "km": 1515, "lat": 18.5289, "lon": 73.8744, "arr": "02:10", "dep": "02:10"}
        ]
    },

    # --- 5. SUPERFAST, MAILS & PREMIER EXPRESSES ---
    {
        "id": "12615",
        "number": "12615",
        "name": "Grand Trunk (GT) Express",
        "type": "Superfast Mail",
        "priority": 2,
        "max_speed": 110.0,
        "origin": "New Delhi (NDLS)",
        "destination": "MGR Chennai Central (MAS)",
        "current_station": "Bhopal Junction (BPL)",
        "next_station": "Itarsi Junction (ET)",
        "lat": 23.2599,
        "lon": 77.4126,
        "progress_pct": 32.0,
        "remaining_distance_km": 1480.0,
        "section_occupancy": "RED",
        "route_junctions": [
            {"name": "New Delhi", "code": "NDLS", "km": 0, "lat": 28.6139, "lon": 77.2090, "arr": "16:10", "dep": "16:10"},
            {"name": "Agra Cantt", "code": "AGC", "km": 195, "lat": 27.1577, "lon": 78.0076, "arr": "18:50", "dep": "18:55"},
            {"name": "VGL Jhansi", "code": "VGLJ", "km": 411, "lat": 25.4484, "lon": 78.5685, "arr": "22:00", "dep": "22:08"},
            {"name": "Bhopal Junction", "code": "BPL", "km": 703, "lat": 23.2599, "lon": 77.4126, "arr": "02:15", "dep": "02:25"},
            {"name": "Itarsi Junction", "code": "ET", "km": 795, "lat": 22.6114, "lon": 77.7656, "arr": "03:55", "dep": "04:05"},
            {"name": "Nagpur Junction", "code": "NGP", "km": 1093, "lat": 21.1458, "lon": 79.0882, "arr": "08:50", "dep": "08:55"},
            {"name": "Balharshah", "code": "BPQ", "km": 1302, "lat": 19.8540, "lon": 79.3414, "arr": "12:15", "dep": "12:20"},
            {"name": "Warangal", "code": "WL", "km": 1545, "lat": 17.9689, "lon": 79.5941, "arr": "15:48", "dep": "15:50"},
            {"name": "Vijayawada Junction", "code": "BZA", "km": 1756, "lat": 16.5062, "lon": 80.6480, "arr": "18:40", "dep": "18:50"},
            {"name": "Nellore", "code": "NLR", "km": 2011, "lat": 14.4426, "lon": 79.9865, "arr": "22:15", "dep": "22:17"},
            {"name": "Chennai Central", "code": "MAS", "km": 2187, "lat": 13.0827, "lon": 80.2707, "arr": "06:20", "dep": "06:20"}
        ]
    },
    {
        "id": "12625",
        "number": "12625",
        "name": "Kerala Express",
        "type": "Superfast Mail",
        "priority": 2,
        "max_speed": 110.0,
        "origin": "New Delhi (NDLS)",
        "destination": "Thiruvananthapuram (TVC)",
        "current_station": "Itarsi Junction (ET)",
        "next_station": "Nagpur Junction (NGP)",
        "lat": 22.6114,
        "lon": 77.7656,
        "progress_pct": 27.0,
        "remaining_distance_km": 2220.0,
        "section_occupancy": "YELLOW",
        "route_junctions": [
            {"name": "New Delhi", "code": "NDLS", "km": 0, "lat": 28.6139, "lon": 77.2090, "arr": "20:10", "dep": "20:10"},
            {"name": "Agra Cantt", "code": "AGC", "km": 195, "lat": 27.1577, "lon": 78.0076, "arr": "22:20", "dep": "22:25"},
            {"name": "Gwalior Junction", "code": "GWL", "km": 313, "lat": 26.2183, "lon": 78.1828, "arr": "23:43", "dep": "23:45"},
            {"name": "VGL Jhansi", "code": "VGLJ", "km": 411, "lat": 25.4484, "lon": 78.5685, "arr": "01:05", "dep": "01:15"},
            {"name": "Bhopal Junction", "code": "BPL", "km": 703, "lat": 23.2599, "lon": 77.4126, "arr": "05:20", "dep": "05:25"},
            {"name": "Itarsi Junction", "code": "ET", "km": 795, "lat": 22.6114, "lon": 77.7656, "arr": "07:00", "dep": "07:10"},
            {"name": "Nagpur Junction", "code": "NGP", "km": 1093, "lat": 21.1458, "lon": 79.0882, "arr": "11:45", "dep": "11:50"},
            {"name": "Balharshah", "code": "BPQ", "km": 1302, "lat": 19.8540, "lon": 79.3414, "arr": "15:20", "dep": "15:25"},
            {"name": "Vijayawada Junction", "code": "BZA", "km": 1756, "lat": 16.5062, "lon": 80.6480, "arr": "21:40", "dep": "21:50"},
            {"name": "Katpadi Junction", "code": "KPD", "km": 2191, "lat": 12.9698, "lon": 79.1350, "arr": "04:10", "dep": "04:15"},
            {"name": "Coimbatore Junction", "code": "CBE", "km": 2568, "lat": 11.0018, "lon": 76.9628, "arr": "09:50", "dep": "09:55"},
            {"name": "Ernakulam Town", "code": "ERN", "km": 2810, "lat": 9.9926, "lon": 76.2954, "arr": "14:15", "dep": "14:20"},
            {"name": "Thiruvananthapuram", "code": "TVC", "km": 3036, "lat": 8.4875, "lon": 76.9525, "arr": "19:00", "dep": "19:00"}
        ]
    },
    {
        "id": "12627",
        "number": "12627",
        "name": "Karnataka Express",
        "type": "Superfast Mail",
        "priority": 2,
        "max_speed": 110.0,
        "origin": "KSR Bengaluru (SBC)",
        "destination": "New Delhi (NDLS)",
        "current_station": "Solapur (SUR)",
        "next_station": "Manmad Junction (MMR)",
        "lat": 17.6599,
        "lon": 75.9064,
        "progress_pct": 27.0,
        "remaining_distance_km": 1750.0,
        "section_occupancy": "GREEN",
        "route_junctions": [
            {"name": "KSR Bengaluru", "code": "SBC", "km": 0, "lat": 12.9716, "lon": 77.5946, "arr": "19:20", "dep": "19:20"},
            {"name": "Dharmavaram", "code": "DMM", "km": 179, "lat": 14.4143, "lon": 77.7214, "arr": "22:18", "dep": "22:20"},
            {"name": "Guntakal Junction", "code": "GTL", "km": 293, "lat": 15.1678, "lon": 77.3756, "arr": "00:10", "dep": "00:15"},
            {"name": "Solapur", "code": "SUR", "km": 657, "lat": 17.6599, "lon": 75.9064, "arr": "05:40", "dep": "05:45"},
            {"name": "Daund Junction", "code": "DD", "km": 844, "lat": 18.4632, "lon": 74.5828, "arr": "08:15", "dep": "08:20"},
            {"name": "Manmad Junction", "code": "MMR", "km": 1082, "lat": 20.2520, "lon": 74.4370, "arr": "13:00", "dep": "13:05"},
            {"name": "Bhusaval Junction", "code": "BSL", "km": 1266, "lat": 21.0454, "lon": 75.7891, "arr": "15:40", "dep": "15:45"},
            {"name": "Itarsi Junction", "code": "ET", "km": 1573, "lat": 22.6114, "lon": 77.7656, "arr": "20:10", "dep": "20:20"},
            {"name": "Bhopal Junction", "code": "BPL", "km": 1665, "lat": 23.2599, "lon": 77.4126, "arr": "21:50", "dep": "21:55"},
            {"name": "VGL Jhansi", "code": "VGLJ", "km": 1957, "lat": 25.4484, "lon": 78.5685, "arr": "01:40", "dep": "01:48"},
            {"name": "Agra Cantt", "code": "AGC", "km": 2173, "lat": 27.1577, "lon": 78.0076, "arr": "04:30", "dep": "04:35"},
            {"name": "New Delhi", "code": "NDLS", "km": 2398, "lat": 28.6139, "lon": 77.2090, "arr": "09:00", "dep": "09:00"}
        ]
    },
    {
        "id": "12841",
        "number": "12841",
        "name": "Coromandel Express",
        "type": "Superfast Mail",
        "priority": 2,
        "max_speed": 130.0,
        "origin": "Howrah Junction (HWH)",
        "destination": "MGR Chennai Central (MAS)",
        "current_station": "Bhubaneswar (BBS)",
        "next_station": "Visakhapatnam (VSKP)",
        "lat": 20.2961,
        "lon": 85.8245,
        "progress_pct": 26.0,
        "remaining_distance_km": 1222.0,
        "section_occupancy": "GREEN",
        "route_junctions": [
            {"name": "Howrah Junction", "code": "HWH", "km": 0, "lat": 22.5858, "lon": 88.3426, "arr": "15:20", "dep": "15:20"},
            {"name": "Kharagpur Junction", "code": "KGP", "km": 115, "lat": 22.3392, "lon": 87.3243, "arr": "17:00", "dep": "17:05"},
            {"name": "Balasore", "code": "BLS", "km": 231, "lat": 21.4934, "lon": 86.9135, "arr": "18:32", "dep": "18:37"},
            {"name": "Bhubaneswar", "code": "BBS", "km": 437, "lat": 20.2961, "lon": 85.8245, "arr": "21:50", "dep": "21:55"},
            {"name": "Visakhapatnam", "code": "VSKP", "km": 881, "lat": 17.7214, "lon": 83.2842, "arr": "04:25", "dep": "04:45"},
            {"name": "Rajahmundry", "code": "RJY", "km": 1082, "lat": 17.0005, "lon": 81.7800, "arr": "07:23", "dep": "07:25"},
            {"name": "Vijayawada Junction", "code": "BZA", "km": 1231, "lat": 16.5062, "lon": 80.6480, "arr": "09:55", "dep": "10:05"},
            {"name": "Nellore", "code": "NLR", "km": 1486, "lat": 14.4426, "lon": 79.9865, "arr": "13:13", "dep": "13:15"},
            {"name": "Chennai Central", "code": "MAS", "km": 1662, "lat": 13.0827, "lon": 80.2707, "arr": "17:00", "dep": "17:00"}
        ]
    },
    {
        "id": "12859",
        "number": "12859",
        "name": "Gitanjali Express",
        "type": "Superfast Mail",
        "priority": 2,
        "max_speed": 110.0,
        "origin": "CSMT Mumbai (CSMT)",
        "destination": "Howrah Junction (HWH)",
        "current_station": "Bhusaval Junction (BSL)",
        "next_station": "Nagpur Junction (NGP)",
        "lat": 21.0454,
        "lon": 75.7891,
        "progress_pct": 23.0,
        "remaining_distance_km": 1515.0,
        "section_occupancy": "YELLOW",
        "route_junctions": [
            {"name": "CSMT Mumbai", "code": "CSMT", "km": 0, "lat": 18.9400, "lon": 72.8353, "arr": "06:00", "dep": "06:00"},
            {"name": "Kalyan Junction", "code": "KYN", "km": 54, "lat": 19.2437, "lon": 73.1355, "arr": "06:52", "dep": "06:55"},
            {"name": "Nashik Road", "code": "NK", "km": 187, "lat": 19.9575, "lon": 73.8322, "arr": "09:20", "dep": "09:25"},
            {"name": "Bhusaval Junction", "code": "BSL", "km": 445, "lat": 21.0454, "lon": 75.7891, "arr": "13:15", "dep": "13:20"},
            {"name": "Akola Junction", "code": "AK", "km": 584, "lat": 20.7002, "lon": 77.0082, "arr": "15:10", "dep": "15:15"},
            {"name": "Nagpur Junction", "code": "NGP", "km": 837, "lat": 21.1458, "lon": 79.0882, "arr": "18:55", "dep": "19:00"},
            {"name": "Raipur Junction", "code": "R", "km": 1139, "lat": 21.2514, "lon": 81.6296, "arr": "23:20", "dep": "23:25"},
            {"name": "Bilaspur Junction", "code": "BSP", "km": 1250, "lat": 22.0797, "lon": 82.1409, "arr": "01:10", "dep": "01:25"},
            {"name": "Tatanagar Junction", "code": "TATA", "km": 1718, "lat": 22.7699, "lon": 86.1884, "arr": "08:15", "dep": "08:25"},
            {"name": "Howrah Junction", "code": "HWH", "km": 1968, "lat": 22.5858, "lon": 88.3426, "arr": "12:30", "dep": "12:30"}
        ]
    },
    {
        "id": "12779",
        "number": "12779",
        "name": "Goa Express",
        "type": "Superfast Mail",
        "priority": 2,
        "max_speed": 110.0,
        "origin": "Vasco da Gama (VSG)",
        "destination": "Hazrat Nizamuddin (NZM)",
        "current_station": "Pune Junction (PUNE)",
        "next_station": "Manmad Junction (MMR)",
        "lat": 18.5289,
        "lon": 73.8744,
        "progress_pct": 24.0,
        "remaining_distance_km": 1640.0,
        "section_occupancy": "GREEN",
        "route_junctions": [
            {"name": "Vasco da Gama", "code": "VSG", "km": 0, "lat": 15.3982, "lon": 73.8113, "arr": "15:00", "dep": "15:00"},
            {"name": "Madgaon Junction", "code": "MAO", "km": 28, "lat": 15.2736, "lon": 73.9580, "arr": "15:40", "dep": "15:45"},
            {"name": "Belagavi", "code": "BGM", "km": 167, "lat": 15.8497, "lon": 74.4977, "arr": "19:00", "dep": "19:05"},
            {"name": "Miraj Junction", "code": "MRJ", "km": 305, "lat": 16.8284, "lon": 74.6465, "arr": "22:15", "dep": "22:20"},
            {"name": "Pune Junction", "code": "PUNE", "km": 584, "lat": 18.5289, "lon": 73.8744, "arr": "04:15", "dep": "04:30"},
            {"name": "Manmad Junction", "code": "MMR", "km": 892, "lat": 20.2520, "lon": 74.4370, "arr": "09:30", "dep": "09:35"},
            {"name": "Bhusaval Junction", "code": "BSL", "km": 1076, "lat": 21.0454, "lon": 75.7891, "arr": "12:00", "dep": "12:05"},
            {"name": "Itarsi Junction", "code": "ET", "km": 1383, "lat": 22.6114, "lon": 77.7656, "arr": "16:45", "dep": "16:55"},
            {"name": "Bhopal Junction", "code": "BPL", "km": 1475, "lat": 23.2599, "lon": 77.4126, "arr": "18:20", "dep": "18:25"},
            {"name": "VGL Jhansi", "code": "VGLJ", "km": 1767, "lat": 25.4484, "lon": 78.5685, "arr": "22:05", "dep": "22:13"},
            {"name": "Agra Cantt", "code": "AGC", "km": 1983, "lat": 27.1577, "lon": 78.0076, "arr": "01:20", "dep": "01:25"},
            {"name": "Hazrat Nizamuddin", "code": "NZM", "km": 2171, "lat": 28.5888, "lon": 77.2534, "arr": "06:25", "dep": "06:25"}
        ]
    },
    {
        "id": "12903",
        "number": "12903",
        "name": "Golden Temple Mail",
        "type": "Superfast Mail",
        "priority": 2,
        "max_speed": 110.0,
        "origin": "Mumbai Central (MMCT)",
        "destination": "Amritsar Junction (ASR)",
        "current_station": "Ratlam Junction (RTM)",
        "next_station": "Kota Junction (KOTA)",
        "lat": 23.3315,
        "lon": 75.0367,
        "progress_pct": 34.0,
        "remaining_distance_km": 1245.0,
        "section_occupancy": "GREEN",
        "route_junctions": [
            {"name": "Mumbai Central", "code": "MMCT", "km": 0, "lat": 18.9696, "lon": 72.8193, "arr": "18:45", "dep": "18:45"},
            {"name": "Borivali", "code": "BVI", "km": 30, "lat": 19.2291, "lon": 72.8573, "arr": "19:15", "dep": "19:18"},
            {"name": "Surat", "code": "ST", "km": 263, "lat": 21.1702, "lon": 72.8311, "arr": "22:25", "dep": "22:30"},
            {"name": "Vadodara Junction", "code": "BRC", "km": 393, "lat": 22.3072, "lon": 73.1812, "arr": "00:08", "dep": "00:18"},
            {"name": "Ratlam Junction", "code": "RTM", "km": 653, "lat": 23.3315, "lon": 75.0367, "arr": "04:15", "dep": "04:25"},
            {"name": "Kota Junction", "code": "KOTA", "km": 920, "lat": 25.2138, "lon": 75.8648, "arr": "07:45", "dep": "07:55"},
            {"name": "Sawai Madhopur", "code": "SWM", "km": 1028, "lat": 25.9928, "lon": 76.3533, "arr": "09:15", "dep": "09:20"},
            {"name": "Mathura Junction", "code": "MTJ", "km": 1244, "lat": 27.4924, "lon": 77.6737, "arr": "12:15", "dep": "12:20"},
            {"name": "Hazrat Nizamuddin", "code": "NZM", "km": 1378, "lat": 28.5888, "lon": 77.2534, "arr": "14:15", "dep": "14:30"},
            {"name": "Ambala Cantt", "code": "UMB", "km": 1576, "lat": 30.3752, "lon": 76.7821, "arr": "17:40", "dep": "17:45"},
            {"name": "Ludhiana Junction", "code": "LDH", "km": 1690, "lat": 30.9010, "lon": 75.8573, "arr": "19:05", "dep": "19:15"},
            {"name": "Amritsar Junction", "code": "ASR", "km": 1826, "lat": 31.6340, "lon": 74.8723, "arr": "21:30", "dep": "21:30"}
        ]
    },
    {
        "id": "12393",
        "number": "12393",
        "name": "Sampoorna Kranti Express",
        "type": "Superfast Mail",
        "priority": 2,
        "max_speed": 130.0,
        "origin": "Rajendra Nagar Patna (RJPB)",
        "destination": "New Delhi (NDLS)",
        "current_station": "Mirzapur (MZP)",
        "next_station": "Kanpur Central (CNB)",
        "lat": 25.1337,
        "lon": 82.5644,
        "progress_pct": 32.0,
        "remaining_distance_km": 680.0,
        "section_occupancy": "GREEN",
        "route_junctions": [
            {"name": "Rajendra Nagar", "code": "RJPB", "km": 0, "lat": 25.5941, "lon": 85.1612, "arr": "19:25", "dep": "19:25"},
            {"name": "Patna Junction", "code": "PNBE", "km": 3, "lat": 25.6022, "lon": 85.1376, "arr": "19:35", "dep": "19:45"},
            {"name": "Pt. DD Upadhyaya", "code": "DDU", "km": 214, "lat": 25.2816, "lon": 83.1189, "arr": "22:20", "dep": "22:30"},
            {"name": "Mirzapur", "code": "MZP", "km": 277, "lat": 25.1337, "lon": 82.5644, "arr": "23:21", "dep": "23:23"},
            {"name": "Kanpur Central", "code": "CNB", "km": 561, "lat": 26.4499, "lon": 80.3319, "arr": "02:25", "dep": "02:30"},
            {"name": "New Delhi", "code": "NDLS", "km": 1002, "lat": 28.6139, "lon": 77.2090, "arr": "07:55", "dep": "07:55"}
        ]
    },
    {
        "id": "12909",
        "number": "12909",
        "name": "Bandra - Nizamuddin Garib Rath",
        "type": "Garib Rath",
        "priority": 2,
        "max_speed": 130.0,
        "origin": "Bandra Terminus (BDTS)",
        "destination": "Hazrat Nizamuddin (NZM)",
        "current_station": "Vadodara Junction (BRC)",
        "next_station": "Ratlam Junction (RTM)",
        "lat": 22.3072,
        "lon": 73.1812,
        "progress_pct": 29.0,
        "remaining_distance_km": 975.0,
        "section_occupancy": "GREEN",
        "route_junctions": [
            {"name": "Bandra Terminus", "code": "BDTS", "km": 0, "lat": 19.0544, "lon": 72.8406, "arr": "17:30", "dep": "17:30"},
            {"name": "Borivali", "code": "BVI", "km": 19, "lat": 19.2291, "lon": 72.8573, "arr": "17:55", "dep": "17:59"},
            {"name": "Surat", "code": "ST", "km": 252, "lat": 21.1702, "lon": 72.8311, "arr": "20:47", "dep": "20:52"},
            {"name": "Vadodara Junction", "code": "BRC", "km": 382, "lat": 22.3072, "lon": 73.1812, "arr": "22:19", "dep": "22:29"},
            {"name": "Ratlam Junction", "code": "RTM", "km": 643, "lat": 23.3315, "lon": 75.0367, "arr": "02:10", "dep": "02:15"},
            {"name": "Kota Junction", "code": "KOTA", "km": 909, "lat": 25.2138, "lon": 75.8648, "arr": "05:25", "dep": "05:35"},
            {"name": "Mathura Junction", "code": "MTJ", "km": 1233, "lat": 27.4924, "lon": 77.6737, "arr": "08:18", "dep": "08:20"},
            {"name": "Hazrat Nizamuddin", "code": "NZM", "km": 1367, "lat": 28.5888, "lon": 77.2534, "arr": "10:15", "dep": "10:15"}
        ]
    }
]

class CorridorSimulator:
    def get_all_trains(self, sim_date: str = "2025-07-15") -> list:
        trains = []
        for t in MOCK_TRAINS:
            current_loc = {"lat": t["lat"], "lon": t["lon"], "section_occupancy": t["section_occupancy"]}
            eta_info = prediction_engine.predict_train_eta(t, current_loc, sim_date)
            combined = copy.deepcopy(t)
            combined["eta_analysis"] = eta_info
            trains.append(combined)
        return trains

    def evaluate_connection_risk(self, incoming_train_id: str, connecting_train_id: str, scheduled_buffer_mins: int = 40, sim_date: str = "2025-07-15") -> dict:
        incoming_t = next((t for t in MOCK_TRAINS if t["id"] == incoming_train_id), MOCK_TRAINS[0])
        connecting_t = next((t for t in MOCK_TRAINS if t["id"] == connecting_train_id), MOCK_TRAINS[1])

        inc_eta = prediction_engine.predict_train_eta(incoming_t, {"lat": incoming_t["lat"], "lon": incoming_t["lon"], "section_occupancy": incoming_t["section_occupancy"]}, sim_date)
        conn_eta = prediction_engine.predict_train_eta(connecting_t, {"lat": connecting_t["lat"], "lon": connecting_t["lon"], "section_occupancy": connecting_t["section_occupancy"]}, sim_date)

        inc_delay = inc_eta["net_delay_mins"]
        conn_delay = conn_eta["net_delay_mins"]

        # Realized buffer = Scheduled Buffer - Incoming Delay + Connecting Delay
        realized_buffer = scheduled_buffer_mins - inc_delay + conn_delay

        if realized_buffer >= 30:
            risk_level = "SAFE"
            risk_color = "#10B981"
            risk_msg = "Safe Connection Window (>30 mins buffer available)."
        elif 15 <= realized_buffer < 30:
            risk_level = "MODERATE RISK"
            risk_color = "#F59E0B"
            risk_msg = "Tight Connection Window (15–30 mins buffer). Fast platform transfer recommended."
        else:
            risk_level = "HIGH RISK / MISSED"
            risk_color = "#EF4444"
            risk_msg = "High Probability of Missed Connection (<15 mins buffer)."

        # Alternatives recommendation
        alternatives = [
            {"train_number": "12626", "train_name": "Kerala Express", "dep_time": "22:10", "available_seats": 42, "buffer_mins": 110},
            {"train_number": "12724", "train_name": "Telangana Express", "dep_time": "23:45", "available_seats": 18, "buffer_mins": 205}
        ]

        return {
            "incoming_train": f"{incoming_t['number']} {incoming_t['name']}",
            "connecting_train": f"{connecting_t['number']} {connecting_t['name']}",
            "junction": "Bhopal Junction (BPL)",
            "scheduled_buffer_mins": scheduled_buffer_mins,
            "realized_buffer_mins": round(realized_buffer, 1),
            "incoming_delay_mins": inc_delay,
            "risk_level": risk_level,
            "risk_color": risk_color,
            "risk_message": risk_msg,
            "suggested_alternatives": alternatives
        }

    def run_what_if_simulation(
        self,
        prioritize_rajdhani: bool = True,
        emergency_block_mins: float = 0.0,
        emergency_block_section: str = "Agra-Gwalior",
        sim_date: str = "2025-07-15"
    ) -> dict:
        results = []
        for t in MOCK_TRAINS:
            is_affected_by_block = ("Agra" in t["current_station"] or "Gwalior" in t["current_station"]) and (emergency_block_mins > 0)
            added_block_mins = emergency_block_mins if is_affected_by_block else 0.0

            current_loc = {"lat": t["lat"], "lon": t["lon"], "section_occupancy": t["section_occupancy"]}
            eta_sim = prediction_engine.predict_train_eta(
                t, 
                current_loc, 
                sim_date=sim_date, 
                precedence_override=prioritize_rajdhani,
                track_block_mins=added_block_mins
            )

            results.append({
                "train_id": t["id"],
                "train_name": t["name"],
                "train_number": t["number"],
                "priority": t["priority"],
                "original_delay_mins": prediction_engine.predict_train_eta(t, current_loc, sim_date)["net_delay_mins"],
                "simulated_delay_mins": eta_sim["net_delay_mins"],
                "delay_delta_mins": round(eta_sim["net_delay_mins"] - prediction_engine.predict_train_eta(t, current_loc, sim_date)["net_delay_mins"], 1),
                "simulated_speed_kmh": eta_sim["effective_speed_kmh"],
                "confidence_score": eta_sim["probabilistic_eta"]["confidence_score_pct"],
                "status_label": eta_sim["probabilistic_eta"]["status_label"]
            })

        return {
            "simulation_parameters": {
                "prioritize_rajdhani": prioritize_rajdhani,
                "emergency_block_mins": emergency_block_mins,
                "emergency_block_section": emergency_block_section,
                "sim_date": sim_date
            },
            "train_impacts": results,
            "overall_corridor_efficiency": "92.4%" if not prioritize_rajdhani and emergency_block_mins == 0 else ("78.5%" if emergency_block_mins > 0 else "88.0%")
        }

    def get_delay_cascade_graph(self) -> dict:
        nodes = [
            {"id": "NDLS", "label": "New Delhi (NDLS)", "delay": 0, "status": "CLEAR"},
            {"id": "AGC", "label": "Agra Cantt (AGC)", "delay": 18, "status": "CAUTION"},
            {"id": "GWL", "label": "Gwalior (GWL)", "delay": 28, "status": "CONGESTED"},
            {"id": "VGLJ", "label": "VGL Jhansi (VGLJ)", "delay": 35, "status": "CONGESTED"},
            {"id": "BPL", "label": "Bhopal (BPL)", "delay": 42, "status": "CRITICAL"}
        ]
        edges = [
            {"source": "NDLS", "target": "AGC", "label": "+18m (Heavy Rain TSR)"},
            {"source": "AGC", "target": "GWL", "label": "+10m (Signal Clearance Hold)"},
            {"source": "GWL", "target": "VGLJ", "label": "+7m (Preceding Rake Congestion)"},
            {"source": "VGLJ", "target": "BPL", "label": "+7m (Platform Overlap Hold)"}
        ]
        return {"nodes": nodes, "edges": edges}

    def get_platform_clash_predictions(self) -> list:
        return [
            {
                "junction": "Bhopal Junction (BPL)",
                "platform": "Platform 2",
                "conflicting_trains": [
                    {"number": "12951", "name": "Mumbai Rajdhani", "eta": "01:32"},
                    {"number": "12615", "name": "GT Express", "eta": "01:38"}
                ],
                "overlap_duration_mins": 12,
                "severity": "HIGH",
                "recommendation": "Reroute GT Express (12615) to Unoccupied Loop Line 3 / Platform 5."
            },
            {
                "junction": "Agra Cantt (AGC)",
                "platform": "Platform 1",
                "conflicting_trains": [
                    {"number": "12002", "name": "Bhopal Shatabdi", "eta": "18:40"},
                    {"number": "12951", "name": "Mumbai Rajdhani", "eta": "18:44"}
                ],
                "overlap_duration_mins": 6,
                "severity": "MODERATE",
                "recommendation": "Hold Shatabdi on Platform 1; receive Rajdhani on Main Through Line 2."
            },
            {
                "junction": "Surat (ST)",
                "platform": "Platform 1",
                "conflicting_trains": [
                    {"number": "20901", "name": "Vande Bharat Express", "eta": "08:58"},
                    {"number": "12009", "name": "Shatabdi Express", "eta": "09:45"}
                ],
                "overlap_duration_mins": 8,
                "severity": "MODERATE",
                "recommendation": "Route Vande Bharat to Platform 1 Through Line; hold preceding freight on Loop 4."
            }
        ]

corridor_simulator = CorridorSimulator()
