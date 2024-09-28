from aigu.imports import *

app = flask.Flask(__name__)

def authGuard():
    loginGuard(); res = cdb.query("select id, userIds, name from groups where app = 'sari'")
    if session["userId"] not in res | cut(1) | joinSt() | aS(set):
        raise flask.ShortCircuit(f"""<script>alert("{ui.trans('You are not authorized to access this website, please contact whoever gave you the link and tell them to authorize you. Logging out...', 'Bạn không có quyền truy cập trang web này, hãy liên hệ người đưa bạn link và kêu họ thêm quyền truy cập cho bạn. Đang đăng xuất...')}"); window.location = "/logout";</script>""")
    return res | filt(op() != "sari_admin", 2) | deref()
def isAdmin(): group = cdb["groups"].lookup(name="sari_admin"); return session["userId"] in group.userIds
def adminGuard():
    loginGuard()
    if not isAdmin(): raise flask.ShortCircuit(f"""<script>alert("{ui.trans('You are not authorized to access this website, please contact whoever gave you the link and tell them to authorize you. Logging out...', 'Bạn không có quyền truy cập trang web này, hãy liên hệ người đưa bạn link và kêu họ thêm quyền truy cập cho bạn. Đang đăng xuất...')}"); window.location = "/logout";</script>""")

@app.route("/report", guard=authGuard)
def fragment_report(): 
    sett = ui.headItem('<svg xmlns="http://www.w3.org/2000/svg" height="24" viewBox="0 -960 960 960" width="24" style="fill: white"><path d="m370-80-16-128q-13-5-24.5-12T307-235l-119 50L78-375l103-78q-1-7-1-13.5v-27q0-6.5 1-13.5L78-585l110-190 119 50q11-8 23-15t24-12l16-128h220l16 128q13 5 24.5 12t22.5 15l119-50 110 190-103 78q1 7 1 13.5v27q0 6.5-2 13.5l103 78-110 190-118-50q-11 8-23 15t-24 12L590-80H370Zm70-80h79l14-106q31-8 57.5-23.5T639-327l99 41 39-68-86-65q5-14 7-29.5t2-31.5q0-16-2-31.5t-7-29.5l86-65-39-68-99 42q-22-23-48.5-38.5T533-694l-13-106h-79l-14 106q-31 8-57.5 23.5T321-633l-99-41-39 68 86 64q-5 15-7 30t-2 32q0 16 2 31t7 30l-86 65 39 68 99-42q22 23 48.5 38.5T427-266l13 106Zm42-180q58 0 99-41t41-99q0-58-41-99t-99-41q-59 0-99.5 41T342-480q0 58 40.5 99t99.5 41Zm-2-140Z"/></svg>', 'https://auth.aigu.vn/settings')
    logout = ui.headItem('<svg xmlns="http://www.w3.org/2000/svg" height="24" viewBox="0 -960 960 960" width="24" style="fill: white"><path d="M200-120q-33 0-56.5-23.5T120-200v-560q0-33 23.5-56.5T200-840h280v80H200v560h280v80H200Zm440-160-55-58 102-102H360v-80h327L585-622l55-58 200 200-200 200Z"/></svg>', '/logout')
    isAdmin_ = isAdmin(); allo = ""
    return ui.main(ui.trans("Ecopark manager", "Công cụ quản lý tưới cây Ecopark"), f"""
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY=" crossorigin=""/>
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js" integrity="sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo=" crossorigin=""></script>
    <style>
        td {{ white-space: nowrap }} tr {{ scroll-margin-top: 80px; }}
        #main {{ flex-direction: row; }}
        #allocation {{ flex-direction: row; }}

        .container_maps{{ padding: 32px 62px; }}
        .title{{font-size: 32px !important; font-weight: 700; color: #00723b; text-align: center;}}
        .h3-title{{font-size 24px; font-weight: 500; margin-bottom: 12px !important; }}

        input{{text-align: center !important; }}

        .header_menu--icon {{ display: none; }}
        .header_menu--contents {{ display: flex; flex-direction: row; }}
        .tabs.active {{ background: #333; }} .tabs:hover {{ background: #444; }} .tabs {{ padding: 8px 12px; background: #222; margin: 0px 1px; height: 56px; display: flex; flex-direction: row; align-items: center; white-space: pre; }}

        @media only screen and (max-width: 767px) {{
            #main {{ flex-direction: column;}}
            #allocation {{ flex-direction: column; }}
            #pad {{ display: none; }} 

            .logo{{ width: 112px !important; height: 40px; }}
            .header_menu {{ position: relative; }}
            .header_menu--icon {{ display: block; font-size: 18px; width: 50px; height: 50px; padding: 8px 10px; display: flex; align-items: center; justify-content: center; cursor: pointer; }}
            .header_menu--contents {{ display: none !important; position: absolute; display: flex; flex-direction: column; top: 58px; left: -2px; }}
            .header_menu--contents button{{ font-size: 14px; }}
            .header_menu:hover .header_menu--contents {{ display: flex !important; }}
            .header_space--delete {{display: none !important; }}

            #working{{margin-left: 12px; }}
            .container_maps{{ padding: 32px 16px; }}
            .title{{font-size: 28px !important; font-weight: 700; color: #00723b; text-align: center;}}
            .h3-title{{font-size 18px; font-weight: 500; }}

        }}

        @media only screen and (min-width: 768px) and (max-width: 991px){{
            .container_maps{{ padding: 32px 16px; }}
            #working{{margin-left: 12px; }}
        }}

    </style>""", f"""
    <div class=" container_maps">
        <h2 class="title">Hệ thống tưới tiêu <p class="title_primary">AIGU Smart Farm</p></h2>
        <div id="main" style="display: flex">
            <div style="flex: 1">{fragment_mapReport()}</div>
            <div id="pad" style="width: 16px"></div>
        </div>
    </div>""", 
    headMode="app:ecopark", headOverride=f"""
    <div style="display: flex; flex-direction: row; background-color: #1e1e1e; color: white; z-index: 10000; position: sticky; top: 0px; padding: 4px 0px; align-items: center">
        <div style="display: flex; flex-direction: row; align-items: center"><img class="logo" src="https://static.aigu.vn/ecopark_logo.png" style="margin-left: 8px; height: 50px"><img class="logo" src ="https://static.aigu.vn/smartfarm_ecopark_black_small.png" style="height: 50px; margin-left: 24px"></div>
        <div class="header_space--delete" style="flex: 1"></div>
        <div class="header_menu" style="display: flex; height: 48px; flex-direction: row; align-items: center">
            <div class="header_menu--contents">
                <button id="tab_remote" class="header_menu--list tabs " onclick="window.location.href='/';">Điều Khiển</button>
                <button id="tab_report" class="header_menu--list tabs active" onclick="window.location.href='/report';">Báo Cáo</button>
                <button id="tab_services" class="header_menu--list tabs" onclick="">Các Gói Dịch Vụ</button>
            </div>
            <div class="header_menu--icon hover:bg-gray-200"><svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 -960 960 960" width="24px" fill="#e8eaed"><path d="M120-240v-80h720v80H120Zm0-200v-80h720v80H120Zm0-200v-80h720v80H120Z"/></svg></div>
        </div>
        {sett}{logout}
    </div>""")

def fragment_mapReport(): return f"""
<style>
    .col-1{{
        width:: 100%;
        display: flex;
        flex-direction: row;
        justify-content: space-between;
    }}

    .map_notes{{ margin-top: 8px; display: flex; justify-content: flex-end; flex-direction: row; align-items: flex-end; margin-bottom: 52px; }}
    .map_notes .circle_note{{ width: 36px; height: 36px; border-radius: 50px; }}
    .map_notes--container{{display: flex; flex-direction: row; align-items: center; margin-left: 24px;}}
    .circle_green{{background-color: green;}}
    .circle_yellow{{background-color: yellow;}}
    .circle_red{{background-color: red;}}
    .text-green{{font-size: 14px; margin-left: 12px; font-weight: 500;}}
    .text-yellow{{font-size: 14px; margin-left: 12px; font-weight: 500;}}
    .text-red{{font-size: 14px; margin-left: 12px; font-weight: 500;}}

    @media only screen and (max-width: 767px) {{
        #map {{height: 400px; }}
        .map_notes{{ margin-top: 8px; display: flex; justify-content: flex-end; flex-direction: column; align-items: flex-start; margin-bottom: 36px; }}
        .map_notes .circle_note{{ width:16px; height: 16px; border-radius: 50px; }}
        .map_notes--container{{display: flex; flex-direction: row; align-items: center; margin-top: 12px; margin-left: 0;}}
    }}

    @media only screen and (min-width: 768px) and (max-width: 991px){{
        .map_notes{{ margin-top: 8px; display: flex; flex-direction: row; justify-content: center; margin-bottom: 36px; }}
    }}

</style>
<div class="box-option">
    <div class="col-1">
        <select id="mapMode" class="select select-bordered w-full max-w-xs" style="margin-top: 12px">
            <option value="road">Đường xá</option>
            <option value="satellite">Vệ tinh</option>
            <option value="temp">Nhiệt độ</option>
        </select>
        <select id="working" class="select select-bordered w-full max-w-xs" style="margin-top: 12px; ">
            <option value="watervolume">Mét khối đã tưới (m³)</option>
            <option value="kgFertilizer">Gam phân bón (g)</option>
            <option value="temperature">Nhiệt độ trung bình (°C)</option>
            <option value="humidity">Độ ẩm trung bình (%)</option>
        </select>
    </div>
</div>
<div id="map" style="width: 100%; height: 600px; margin-top: 12px"></div>
<div class="map_notes">
    <div class="map_notes--container">
        <div class="circle_note circle_green"></div>
        <p class="text-green">Mức nước an toàn</p>
    </div>
    <div class="map_notes--container">
        <div class="circle_note circle_yellow"></div>
        <p class="text-yellow">Mức nước cảnh báo</p>
    </div>
    <div class="map_notes--container">
        <div class="circle_note circle_red"></div>
        <p class="text-red">Mức nước báo động</p>
    </div>
</div>
<div>{fragment_detailsReports()}</div>
<script>
    dS = (x) => document.querySelector(x)
    valves = {valves()}; map = L.map('map').setView([20.960800, 105.935004], 14); name2Circle = {{}};
    timeouts = {timeouts()};
    setTimeout(() => {{ map._onResize(); }}, 100); setTimeout(() => {{ map._onResize(); }}, 300); setTimeout(() => {{ map._onResize(); }}, 1000);

    dS("#mapMode").onchange = () => {{
        const value = dS("#mapMode").value;
        if (value === "road") L.tileLayer('https://openstreetmap.proxy.aigu.vn/{{z}}/{{x}}/{{y}}.png', {{ maxZoom: 19 }}).addTo(map);
        else if (value === "satellite") L.tileLayer('https://mt0.google.com/vt/lyrs=s&x={{x}}&y={{y}}&z={{z}}', {{ maxZoom: 19 }}).addTo(map);
        else if (value === "temp") L.tileLayer('https://sari.aigu.vn/tile/temp/{{x}}/{{y}}/{{z}}', {{ maxZoom: 19 }}).addTo(map);
    }}
    L.tileLayer('https://openstreetmap.proxy.aigu.vn/{{z}}/{{x}}/{{y}}.png', {{ maxZoom: 19 }}).addTo(map);

    function waterVolume() {{
        return Math.floor(Math.random() * 9) + 1;
    }}

    function kgFertilizer() {{
        return Math.floor(Math.random() * 9) + 1;
    }}
    
    function temp() {{
        return (Math.random() * 10 + 25).toFixed(1)
    }}
    
    function rh() {{
        return Math.floor(Math.random() * 20) + 70
    }}
    
    for (const [idx, name, isPump, lat, lng] of valves) {{
        eps = 1e-4;

        let volume = waterVolume();

        let color = 'red';
        if(volume < 3) {{
            color = 'green';
        }}else if(volume > 3 && volume <7){{color='yellow'}}
        else if(volume >7){{color='red'}}

        if (!isPump) shape = L.circle([lat, lng], {{ color: color, fillColor: color, fillOpacity: 0.5, radius: 20 }}).bindTooltip(`Lượng nước đã tưới: ${{volume}} m³`).addTo(map);
        name2Circle[name] = shape; shape.on("click", (e) => handleClick(idx, false));
        L.marker([lat, lng], {{icon: L.divIcon({{ className: 'custom-icon', html: `<div class="custom-label" onclick="handleClick(${{idx}}, false)" style="display: none"><nobr>${{volume}} m³</nobr></div>` }})}}).addTo(map);
    }}

    dS("#working").onchange = () => {{
        const value = dS("#working").value;
        for (const [idx, name, isPump, lat, lng] of valves) {{
            let shape = name2Circle[name];
            let newContent = "";

            if (value === "watervolume") {{
                let volume = waterVolume();
                newContent = `Lượng nước đã tưới: ${{volume}} m³`;
            }} else if (value === "kgFertilizer") {{
                let amount = kgFertilizer();
                newContent = `Lượng phân bón: ${{amount}} g`;
            }} else if (value === "temperature") {{
                let temperature = temp();
                newContent = `Nhiệt độ trung bình: ${{temperature}} °C`;
            }} else if (value === "humidity") {{
                let humidity = rh();
                newContent = `Độ ẩm trung bình: ${{humidity}} %`;
            }}     
            
            shape.bindTooltip(newContent).openTooltip();   
        }}
    }}

    map.on('zoomend', () => {{
        var zoomLevel = map.getZoom();
        if (zoomLevel >= 17) Array.from(document.querySelectorAll('.custom-label')).map((x) => {{ x.style.display = 'block'; }});
        else Array.from(document.querySelectorAll('.custom-label')).map((x) => {{ x.style.display = 'none'; }});
    }});
   
    function handleClick(idx, shorted=true) {{
        selectedValve = idx; valve = valves.filter((row) => row[0] == idx)[0]; document.querySelector("#detailsReports").style.display = "flex"
        document.querySelector("#detailsReports>div>div>h2").innerHTML = `<nobr style="font-size: 32px; font-weight: 700; ; color: #00723b">{ui.trans('Valve', 'Van')} ${{valve[1]}}</nobr>`;
        if (!shorted) {{
            valvesTableSelectCb((row) => row[0] == idx);
            map.setView([valve[3], valve[4]]);
        }}
    }}
</script>"""

def fragment_detailsReports(): return f"""
<style>
    #details {{ flex-direction: row;  padding: 32px 62px; }}

    @media only screen and (max-width: 767px) {{
        #details {{ flex-direction: row;  padding: 32px 16px; }}
        .detailsReports--container{{padding: 16px !important; }}
    }}
    @media only screen and (min-width: 768px) and (max-width: 991px){{
        #details {{ flex-direction: row;  padding: 32px 16px; }}
        .detailsReports--container{{padding: 32px !important; }}
    }}
</style>
<div id="detailsReports" style="display: none; margin-top: 8px;">
    <div class="detailsReports--container" style="display: flex; flex-direction: column; flex: 1; box-shadow: 4px 4px 12px #888888; padding: 46px; border-radius: 24px; ">
        <div style="display: flex; flex-direction: row; margin-bottom: 8px; align-items: center; overflow-x: auto; justify-content: center; ">
            <h2></h2>
        </div>
        
       {fragment_setpoint()}{fragment_fertilizer()}{fragment_waterVolumeTiming()}
    </div>
    <div></div>
</div>"""

def fragment_waterVolumeTiming(): return f"""
<style>
    #waterVolumeTiming > * {{ align-self: center; }}
</style>
<h3 class="h3-title">Lượng nước đã tưới trong </h3>
<div id="setpoint" style="display: grid; grid-template-columns: min-content min-content min-content; margin-bottom: 24px; ">
    <div style="white-space: pre; margin-bottom: 8px;">Ngày</div>
    <input type="text" class="input input-bordered" style="width: 100px; margin-left: 8px; margin-bottom: 8px;" value="10" />
    <div style="margin-left: 8px; margin-bottom: 8px;">L</div>
    <div style="white-space: pre; margin-bottom: 8px;">Tuần</div>
    <input type="text" class="input input-bordered" style="width: 100px; margin-left: 8px; margin-bottom: 8px;" value="20" />
    <div style="margin-left: 8px; margin-bottom: 8px;">L</div>
    <div style="white-space: pre; margin-bottom: 8px;">Tháng</div>
    <input type="text" class="input input-bordered" style="width: 100px; margin-left: 8px; margin-bottom: 8px;" value="50" />
    <div style="margin-left: 8px; margin-bottom: 8px;">L</div>
</div>"""

def fragment_graph(): return f"""
<h2>Cảm biến</h2>
<div id="graph">
    <div style="position: relative; height: 30vh"><canvas id="fr_chart1"></canvas></div>
    <div style="position: relative; height: 30vh"><canvas id="fr_chart2"></canvas></div>
    <div style="position: relative; height: 30vh"><canvas id="fr_chart3"></canvas></div>
</div>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script>
    fr_data = []; fr_pins = [];

    setInterval(async () => {{
        res = await (await fetch(`/fr_read`)).json();
        window.ress = res; if (!res.payload.dPins) return;
        
        for (const e of res.data) fr_data.push([e[0], [...e[1], ...e[2]]]);
        const lengthLimit = 1000; if (fr_data.length > lengthLimit) fr_data = fr_data.slice(fr_data.length-lengthLimit);
        chart1.data.labels = fr_data.map(x => (x[0] - fr_data[0][0])/1000);
        chart2.data.labels = fr_data.map(x => (x[0] - fr_data[0][0])/1000);
        chart3.data.labels = fr_data.map(x => (x[0] - fr_data[0][0])/1000);
        chart1.data.datasets[0].data = fr_data.map(x => x[1][0]);
        chart2.data.datasets[0].data = fr_data.map(x => x[1][1]);
        chart3.data.datasets[0].data = fr_data.map(x => x[1][2]);
        chart1.update();chart2.update();chart3.update();
    }}, 1000);
    chart1 = new Chart(dS("#fr_chart1"), {{
        type: "line",
        data: {{ labels: [], datasets: [] }},
        options: {{ scales: {{ x: {{ type: "linear" }} }} }}
    }});
    chart2 = new Chart(dS("#fr_chart2"), {{
        type: "line",
        data: {{ labels: [], datasets: [] }},
        options: {{ scales: {{ x: {{ type: "linear" }} }} }}
    }});
    chart3 = new Chart(dS("#fr_chart3"), {{
        type: "line",
        data: {{ labels: [], datasets: [] }},
        options: {{ scales: {{ x: {{ type: "linear" }} }} }}
    }});
    chart1.data.labels = []; chart1.data.datasets = [{{label: "Nhiệt độ (C)", data: []}}]; chart1.update();
    chart2.data.labels = []; chart2.data.datasets = [{{label: "Độ ẩm không khí (%)", data: []}}]; chart2.update();
    chart3.data.labels = []; chart3.data.datasets = [{{label: "Độ ẩm đất", data: []}}]; chart3.update();
</script>"""

@app.route("/", guard=authGuard)
def index():
    sett = ui.headItem('<svg xmlns="http://www.w3.org/2000/svg" height="24" viewBox="0 -960 960 960" width="24" style="fill: white"><path d="m370-80-16-128q-13-5-24.5-12T307-235l-119 50L78-375l103-78q-1-7-1-13.5v-27q0-6.5 1-13.5L78-585l110-190 119 50q11-8 23-15t24-12l16-128h220l16 128q13 5 24.5 12t22.5 15l119-50 110 190-103 78q1 7 1 13.5v27q0 6.5-2 13.5l103 78-110 190-118-50q-11 8-23 15t-24 12L590-80H370Zm70-80h79l14-106q31-8 57.5-23.5T639-327l99 41 39-68-86-65q5-14 7-29.5t2-31.5q0-16-2-31.5t-7-29.5l86-65-39-68-99 42q-22-23-48.5-38.5T533-694l-13-106h-79l-14 106q-31 8-57.5 23.5T321-633l-99-41-39 68 86 64q-5 15-7 30t-2 32q0 16 2 31t7 30l-86 65 39 68 99-42q22 23 48.5 38.5T427-266l13 106Zm42-180q58 0 99-41t41-99q0-58-41-99t-99-41q-59 0-99.5 41T342-480q0 58 40.5 99t99.5 41Zm-2-140Z"/></svg>', 'https://auth.aigu.vn/settings')
    logout = ui.headItem('<svg xmlns="http://www.w3.org/2000/svg" height="24" viewBox="0 -960 960 960" width="24" style="fill: white"><path d="M200-120q-33 0-56.5-23.5T120-200v-560q0-33 23.5-56.5T200-840h280v80H200v560h280v80H200Zm440-160-55-58 102-102H360v-80h327L585-622l55-58 200 200-200 200Z"/></svg>', '/logout')
    isAdmin_ = isAdmin(); allo = ""
    return ui.main(ui.trans("Ecopark manager", "Công cụ quản lý tưới cây Ecopark"), f"""
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY=" crossorigin=""/>
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js" integrity="sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo=" crossorigin=""></script>
<style>
    td {{ white-space: nowrap }} tr {{ scroll-margin-top: 80px; }}
    #main {{ flex-direction: row; }}
    #allocation {{ flex-direction: row; }}

    .header_menu--icon {{ display: none; }}
    .header_menu--contents {{ display: flex; flex-direction: row; }}
    .tabs.active {{ background: #333; }} .tabs:hover {{ background: #444; }} .tabs {{ padding: 8px 12px; background: #222; margin: 0px 1px; height: 56px; display: flex; flex-direction: row; align-items: center; white-space: pre; }}

    @media only screen and (max-width: 767px) {{
        #main {{ flex-direction: column;}}
        #allocation {{ flex-direction: column; }}
        #pad {{ display: none; }} 

        .logo{{ width: 112px !important; height: 40px; }}
        .header_menu {{ position: relative; }}
        .header_menu--icon {{ display: block; font-size: 18px; width: 50px; height: 50px; padding: 8px 10px; display: flex; align-items: center; justify-content: center; cursor: pointer; }}
        .header_menu--contents {{ display: none !important; position: absolute; display: flex; flex-direction: column; top: 58px; left: -2px; }}
        .header_menu--contents button{{ font-size: 14px; }}
        .header_menu:hover .header_menu--contents {{ display: flex !important; }}
        .header_space--delete {{display: none !important; }}
    }}

    @media only screen and (max-width: 700px) {{
        #main {{ flex-direction: column; }}
        #allocation {{ flex-direction: column; }}
        #pad {{ display: none; }} }}
</style>""", f"""
<h2>{ui.trans('Ecopark manager', 'Quản lý tưới cây Ecopark')}</h2>
<div id="main" style="display: flex">
    <div style="flex: 1">{fragment_main()}</div>
    <div id="pad" style="width: 16px"></div>
    <div style="flex: 1; overflow-x: auto">{fragment_valvesTable(isAdmin_)}</div>
</div>{fragment_details()}{allo}""", headMode="app:ecopark", headOverride=f"""
<div style="display: flex; flex-direction: row; background-color: #1e1e1e; color: white; z-index: 10000; position: sticky; top: 0px; padding: 4px 0px; align-items: center">
    <div style="display: flex; flex-direction: row; align-items: center"><img class="logo" src="https://static.aigu.vn/ecopark_logo.png" style="margin-left: 8px; height: 50px"><img class="logo" src ="https://static.aigu.vn/smartfarm_ecopark_black_small.png" style="height: 50px; margin-left: 24px"></div>
    <div class="header_space--delete" style="flex: 1"></div>
    <div class="header_menu" style="display: flex; height: 48px; flex-direction: row; align-items: center">
        <div class="header_menu--contents">
            <button id="tab_remote" class="header_menu--list tabs active" onclick="window.location.href='/';">Điều Khiển</button>
            <button id="tab_report" class="header_menu--list tabs" onclick="window.location.href='/report';">Báo Cáo</button>
            <button id="tab_services" class="header_menu--list tabs" onclick="">Các Gói Dịch Vụ</button>
        </div>
        <div class="header_menu--icon hover:bg-gray-200"><svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 -960 960 960" width="24px" fill="#e8eaed"><path d="M120-240v-80h720v80H120Zm0-200v-80h720v80H120Zm0-200v-80h720v80H120Z"/></svg></div>
    </div>
    {sett}{logout}
</div>
<script>
   
</script>""")
edge = 3000
p_temps = cat("p_temps_3000.pth", False) | aS(dill.loads)
# p_rhs = cat("p_rhs.pth", False) | aS(dill.loads)
x1 = 13010/2**14; x2 = 13015/2**14; y1 = 7213/2**14; y2 = 7218/2**14
tiles = {}
def getTile(x,y,z):
    s = f"{x};{y};{z}"
    if s not in tiles: tiles[s] = cat(f"https://mt2.google.com/vt/lyrs=s&x={x}&y={y}&z={z}", False) | toImg()
    return tiles[s]
mapLock = threading.Lock()
def getHeatmap(arr, cmap="coolwarm"):
    with mapLock:
        plt.imshow(arr, cmap=cmap, extent=[0, 256, 0, 256], vmin=p_temps | toMin(), vmax=p_temps | toMax())
        plt.axis('off'); im = plt.gcf() | toImg()
    return im.resize((256, 256), PIL.Image.Resampling.BICUBIC)

tileLock = threading.Lock()
@app.route("/tile/temp/<x>/<y>/<z>")
def _tile(x, y, z):
    with tileLock:
        x = int(x); y = int(y); z = int(z); s = f"{x};{y};{z}"
        arr = p_temps[int(edge*(y/2**z-y1)/(y2-y1)):int(edge*((y+1)/2**z-y1)/(y2-y1)), int(edge*(x/2**z-x1)/(x2-x1)):int(edge*((x+1)/2**z-x1)/(x2-x1))]
        heatmap = getHeatmap(arr)
        tile = getTile(x, y, z); return PIL.Image.blend(tile, heatmap, 0.7) | toBytes(), 200, {"Content-Type": "image/jpg"}

def fragment_main(): return f"""
<select id="viewMode" class="select select-bordered w-full max-w-xs" style="margin-top: 12px; display: none">
    <option value="watering" selected>{ui.trans('Watering', 'Đang tưới')}</option>
    <option value="online">{ui.trans('Online', 'Đang bật')}</option>
</select>
<select id="mapMode" class="select select-bordered w-full max-w-xs" style="margin-top: 12px">
    <option value="road">Đường xá</option>
    <option value="satellite">Vệ tinh</option>
    <option value="temp">Nhiệt độ</option>
</select><div id="map" style="width: 100%; height: 450px; margin-top: 12px"></div>
<script>
    dS = (x) => document.querySelector(x)
    valves = {valves()}; map = L.map('map').setView([20.960800, 105.935004], 14); name2Circle = {{}};
    timeouts = {timeouts()};
    setTimeout(() => {{ map._onResize(); }}, 100); setTimeout(() => {{ map._onResize(); }}, 300); setTimeout(() => {{ map._onResize(); }}, 1000);

    dS("#mapMode").onchange = () => {{
        const value = dS("#mapMode").value;
        if (value === "road") L.tileLayer('https://openstreetmap.proxy.aigu.vn/{{z}}/{{x}}/{{y}}.png', {{ maxZoom: 19 }}).addTo(map);
        else if (value === "satellite") L.tileLayer('https://mt0.google.com/vt/lyrs=s&x={{x}}&y={{y}}&z={{z}}', {{ maxZoom: 19 }}).addTo(map);
        else if (value === "temp") L.tileLayer('https://sari.aigu.vn/tile/temp/{{x}}/{{y}}/{{z}}', {{ maxZoom: 19 }}).addTo(map);
    }}
    L.tileLayer('https://openstreetmap.proxy.aigu.vn/{{z}}/{{x}}/{{y}}.png', {{ maxZoom: 19 }}).addTo(map);
    for (const [idx, name, isPump, lat, lng] of valves) {{
        eps = 1e-4;
        if (isPump) shape = L.polygon([[lat+eps, lng-eps], [lat+eps, lng+eps], [lat-eps, lng]], {{ color: 'red', fillColor: 'red', fillOpacity: 0.5, radius: 8 }}).addTo(map);
        else shape = L.circle([lat, lng], {{ color: 'red', fillColor: 'red', fillOpacity: 0.5, radius: 8 }}).addTo(map);
        name2Circle[name] = shape; shape.on("click", (e) => handleClick(idx, false));
        L.marker([lat, lng], {{icon: L.divIcon({{ className: 'custom-icon', html: `<div class="custom-label" onclick="handleClick(${{idx}}, false)" style="display: none"><nobr>${{name}}</nobr></div>` }})}}).addTo(map);
    }}
    map.on('zoomend', () => {{
        var zoomLevel = map.getZoom();
        if (zoomLevel >= 17) Array.from(document.querySelectorAll('.custom-label')).map((x) => {{ x.style.display = 'block'; }});
        else Array.from(document.querySelectorAll('.custom-label')).map((x) => {{ x.style.display = 'none'; }});
    }});
    viewMode = document.querySelector("#viewMode"); uptime = null;
    // https://ecopark.vsi.com.vn/api/LoraNode/LoraViewNode
    // setInterval(async () => {{ window.uptime = (await (await fetch("http://171.244.39.112:13579/api/LoraNode/LoraViewNode")).json()).filter((x) => 1 <= x.id && x.id <= 49); }}, 1000);
    setInterval(async () => {{ window.uptime = (await (await fetch("/status")).json()).filter((x) => 1 <= x.id && x.id <= 49); }}, 1000);
    setInterval(async () => {{ window.timeouts = await (await fetch("/timeouts")).json(); }}, 1000);
    setInterval(async () => {{
        if (!uptime) return;
        for (const [name,circle] of Object.entries(name2Circle)) {{
            const [a, b] = name.replace("#", "").split("-").map(x => parseInt(x));
            const res = uptime.filter(x => x.id === a); let activated = false;
            if (res.length > 0 && res[0].status === 0) {{ if ((viewMode.value === "watering" && res[0][`s${{b}}`] === 0) || viewMode.value === "online") activated = true; }}
            if (activated) circle.setStyle({{ color: "green", "fillColor": "green" }}); else circle.setStyle({{ color: "red", "fillColor": "red" }});
        }};
    }}, 100);
    function handleClick(idx, shorted=true) {{
        selectedValve = idx; valve = valves.filter((row) => row[0] == idx)[0]; document.querySelector("#details").style.display = "flex"
        document.querySelector("#details>div>div>h2").innerHTML = `<nobr>{ui.trans('Valve', 'Van')} ${{valve[1]}}</nobr>`;
        if (!shorted) {{
            valvesTableSelectCb((row) => row[0] == idx);
            map.setView([valve[3], valve[4]]);
        }}
    }}
</script>"""
def fragment_details(): return f"""
<style>
    #details {{ flex-direction: row; }}
    @media only screen and (max-width: 700px) {{
    #details {{ flex-direction: column; }} }}
</style>
<div id="details" style="display: none; margin-top: 8px;">
    <div style="display: flex; flex-direction: column; flex: 1">
        <div style="display: flex; flex-direction: row; margin-bottom: 8px; align-items: center; overflow-x: auto">
            <h2></h2>
            <button class="btn" onclick="turnOn(0)" style="margin-left: 12px; margin-right: 8px">{ui.trans('Turn on', 'Bật')}</button>
            <button class="btn" onclick="turnOff()" style="margin-right: 8px">{ui.trans('Turn off', 'Tắt')}</button>
            <div id="remaining"></div>
        </div>
        <div style="display: flex; flex-direction: row; overflow-x: auto">
            <button class="btn" onclick="turnOn(2*60)" style="margin-right: 8px">1'</button>
            <button class="btn" onclick="turnOn(5*60)" style="margin-right: 8px">2'</button>
            <button class="btn" onclick="turnOn(10*60)" style="margin-right: 8px">3'</button>
            <button class="btn" onclick="turnOn(15*60)" style="margin-right: 8px">5'</button>
            <button class="btn" onclick="turnOn(20*60)" style="margin-right: 8px">10'</button>
            <button class="btn" onclick="turnOn(30*60)" style="margin-right: 8px">20'</button>
            <button class="btn" onclick="turnOn(40*60)" style="margin-right: 8px">30'</button>
            <button class="btn" onclick="turnOn(50*60)" style="margin-right: 8px">40'</button>
        </div>
        {fragment_timer()}{fragment_setpoint()}
    </div>
    <div style="flex: 1">{fragment_fertilizer()}</div>
</div>
<script>
    async function turnOn(time)  {{ await wrapToastReq(fetch(`/turnOn/${{selectedValve}}/${{time}}`));  }}
    async function turnOff() {{ await wrapToastReq(fetch(`/turnOff/${{selectedValve}}`)); }}
    remaining = document.querySelector("#remaining"); selectedValve = null;
    setInterval(() => {{
        remaining.innerHTML = "";
        if (selectedValve) {{
            rows = timeouts.filter(([x,y]) => x == selectedValve);
            if (rows.length === 1) {{
                delta = rows[0][1] - Date.now()/1000; if (delta < 0) return;
                remaining.innerHTML = "{ui.trans("Turns off in: ", "Tắt sau: ")}" + (delta > 60 ? `${{Math.floor(delta/60)}}'${{Math.round(delta%60)}}s` : `${{Math.round(delta)}}s`);
            }}
        }}
    }}, 100);
</script>"""

meta = {"timerDuration": 120, "timerTimes": [6, 7, 11], "spRh": [75, 90], "spTemp": [20, 38]}
def fragment_timer():
    isOn = lambda secs: "" if secs == meta["timerDuration"] else "btn-outline"
    isSlice = lambda hour: "" if hour in meta["timerTimes"] else "btn-outline"
    return f"""
<style>
    .btn-c1 {{ color: black; background: #73bc4c; border-color: #73bc4c; }}
    .btn-c1.btn-outline {{ background: white; }}
    .btn-c1:hover {{ background: green; border-color: green; }}
    .btn-c2 {{ color: black; background: #e2f3d8; border-color: #e2f3d8; }}
    .btn-c2.btn-outline {{ background: white; }}
    .btn-c2:hover {{ background: green; border-color: green; }}
</style>
<h3>Hẹn giờ( Tưới theo phút)</h3>
<div>
    <button id="t_60"   class="btn btn-c1 {isOn(60)}" style="margin-right: 8px">1'</button>
    <button id="t_120"  class="btn btn-c1 {isOn(120)}" style="margin-right: 8px">2'</button>
    <button id="t_300"  class="btn btn-c1 {isOn(300)}" style="margin-right: 8px">5'</button>
    <button id="t_600"  class="btn btn-c1 {isOn(600)}" style="margin-right: 8px">10'</button>
    <button id="t_1200" class="btn btn-c1 {isOn(1200)}" style="margin-right: 8px">20'</button>
</div>
<h3>Các giờ tưới trong ngày</h3>
<div id="timer_times" style="display: grid; grid-template-columns: 50px 50px 50px 50px 50px 50px; margin-top: 8px">
    <button id="t0"  class="btn btn-c2 {isSlice(0)}">0</button>
    <button id="t1"  class="btn btn-c2 {isSlice(1)}">1</button>
    <button id="t2"  class="btn btn-c2 {isSlice(2)}">2</button>
    <button id="t3"  class="btn btn-c2 {isSlice(3)}">3</button>
    <button id="t4"  class="btn btn-c2 {isSlice(4)}">4</button>
    <button id="t5"  class="btn btn-c2 {isSlice(5)}">5</button>
    <button id="t6"  class="btn btn-c2 {isSlice(6)}">6</button>
    <button id="t7"  class="btn btn-c2 {isSlice(7)}">7</button>
    <button id="t8"  class="btn btn-c2 {isSlice(8)}">8</button>
    <button id="t9"  class="btn btn-c2 {isSlice(9)}">9</button>
    <button id="t10" class="btn btn-c2 {isSlice(10)}">10</button>
    <button id="t11" class="btn btn-c2 {isSlice(11)}">11</button>
    <button id="t12" class="btn btn-c2 {isSlice(12)}">12</button>
    <button id="t13" class="btn btn-c2 {isSlice(13)}">13</button>
    <button id="t14" class="btn btn-c2 {isSlice(14)}">14</button>
    <button id="t15" class="btn btn-c2 {isSlice(15)}">15</button>
    <button id="t16" class="btn btn-c2 {isSlice(16)}">16</button>
    <button id="t17" class="btn btn-c2 {isSlice(17)}">17</button>
    <button id="t18" class="btn btn-c2 {isSlice(18)}">18</button>
    <button id="t19" class="btn btn-c2 {isSlice(19)}">19</button>
    <button id="t20" class="btn btn-c2 {isSlice(20)}">20</button>
    <button id="t21" class="btn btn-c2 {isSlice(21)}">21</button>
    <button id="t22" class="btn btn-c2 {isSlice(22)}">22</button>
    <button id="t23" class="btn btn-c2 {isSlice(23)}">23</button>
</div>
<script>
    dS = (x) => document.querySelector(x);
    durations = [dS("#t_60"), dS("#t_120"), dS("#t_300"), dS("#t_600"), dS("#t_1200")];
    times = [...Array(24).keys()].map(x => dS(`#t${{x}}`));
    for (const durD of durations) {{
        durD.onclick = async () => {{
            const res = durD.classList.contains("btn-outline");
            // const res = await (await wrapToastReq(fetch("/_timer/duration/" + durD.id), {{success: null, info: null}})).text();
            for (const durDd of durations) {{ durDd.classList.add("btn-outline"); }}
            if (res) durD.classList.remove("btn-outline");
        }}
    }}
    for (const timeD of times) {{
        timeD.onclick = async () => {{
            // await wrapToastReq(fetch("/_timer/slice/" + timeD.id), {{success: null, info: null}})
            if (timeD.classList.contains("btn-outline")) {{
                timeD.classList.remove("btn-outline");
            }} else {{ timeD.classList.add("btn-outline"); }}
        }}
    }}
</script>"""

def fragment_setpoint(): return f"""
<style>#setpoint > * {{ align-self: center; }}</style>
<h3 class="h3-title">Khoảng độ ẩm/nhiệt độ</h3>
<div id="setpoint" style="display: grid; grid-template-columns: min-content min-content min-content min-content min-content; margin-bottom: 24px; ">
    <div style="margin-bottom: 8px;">Độ&nbsp;ẩm</div>
    <input id="rh1" type="text" class="input input-bordered" style="width: 100px; margin-left: 8px; margin-bottom: 8px;" value="{meta['spRh'][0]}" />
    <div style="margin: 0px 8px; margin-bottom: 8px;"> - </div>
    <input id="rh2" type="text" class="input input-bordered" style="width: 100px; margin-bottom: 8px;" value="{meta['spRh'][1]}" />
    <div style="margin-left: 8px; margin-bottom: 8px;"> % </div>
    <div style="margin-bottom: 8px;">Nhiệt&nbsp;độ</div>
    <input id="temp1" type="text" class="input input-bordered" style="width: 100px; margin-left: 8px; margin-bottom: 8px;" value="{meta['spTemp'][0]}" />
    <div style="margin: 0px 8px; margin-bottom: 8px;"> - </div>
    <input id="temp2" type="text" class="input input-bordered" style="width: 100px; margin-bottom: 8px;" value="{meta['spTemp'][1]}" />
    <div style="margin-left: 8px; margin-bottom: 8px;"> C </div>
</div>"""

def fragment_fertilizer(): return f"""
<h3 class="h3-title">Hỗn hợp phân bón</h3>
<div id="setpoint" style="display: grid; grid-template-columns: min-content min-content min-content; margin-bottom: 24px; ">
    <div style="white-space: pre; margin-bottom: 8px;">Nồng độ</div>
    <input type="text" class="input input-bordered" style="width: 100px; margin-left: 8px; margin-bottom: 8px;" value="10" />
    <div style="margin-left: 8px; margin-bottom: 8px;">g/L</div>
    <div style="white-space: pre; margin-bottom: 8px;">Ni tơ</div>
    <input type="text" class="input input-bordered" style="width: 100px; margin-left: 8px; margin-bottom: 8px;" value="20" />
    <div style="margin-left: 8px; margin-bottom: 8px;">%</div>
    <div style="white-space: pre; margin-bottom: 8px;">Phốt pho</div>
    <input type="text" class="input input-bordered" style="width: 100px; margin-left: 8px; margin-bottom: 8px;" value="50" />
    <div style="margin-left: 8px; margin-bottom: 8px;">%</div>
    <div style="white-space: pre; ">Kali</div>
    <input type="text" class="input input-bordered" style="width: 100px; margin-left: 8px" value="30" />
    <div style="margin-left: 8px; ">%</div>
</div>"""

def timerThread():
    while True:
        try:
            timeouts = db["timeouts"].select("select * from timeouts")
            for to in timeouts:
                if time.time() > to.timeout: turnOff(to.valveId)
        except: pass
        time.sleep(3)
threading.Thread(target=timerThread).start()

@app.route("/status")
def status():
    return requests.get("http://171.244.39.112:13579/api/LoraNode/LoraViewNode").text

@app.route("/turnOn/<valveId>/<seconds>", guard=authGuard)
def turnOn(valveId, seconds):
    valve = db["valves"][int(valveId)]; name = valve.name.strip("#"); a, b = name.split("-") | apply(int); s = [2]*10; s[b-1] = 0; seconds = int(seconds)
    res = requests.post("http://171.244.39.112:13579/api/LoraNode/LoRaControl", json={ "id": a, "s": s | join(""), "tokenkey": "N9PgTKx/cjhWtm9/Sv7OtRphMoAsMjoCaoDaevu8VYSn9U+rJz4gdQ==" })
    if res.ok:
        if seconds > 0:
            e = db["timeouts"].lookup(valveId=valve.id)
            if e: e.timeout = time.time() + seconds
            else: db["timeouts"].insert(valveId=valve.id, timeout=time.time() + seconds)
        return "ok"
    else: raise Exception(res.text)
@app.route("/turnOff/<valveId>", guard=authGuard)

def _turnOff(valveId): return turnOff(valveId)
def turnOff(valveId):
    print(f"turnOff: {valveId}")
    valve = db["valves"][int(valveId)]
    name = valve.name.strip("#"); a, b = name.split("-") | apply(int); s = [2]*10; s[b-1] = 1
    # https://ecopark.vsi.com.vn/api/LoraNode/LoRaControl UPQu1IbvNh4wgR1+57SsRpCcqnkkPScSEAV60nlx07s+Oua6JBEzmg==
    res = requests.post("http://171.244.39.112:13579/api/LoraNode/LoRaControl", json={ "id": a, "s": s | join(""), "tokenkey": "UPQu1IbvNh4wgR1+57SsRpCcqnkkPScSEAV60nlx07s+Oua6JBEzmg==" })
    if res.ok:
        e = db["timeouts"].lookup(valveId=valve.id)
        if e: del db["timeouts"][e.id]
        return "ok"
    else: raise Exception(res.text)
@app.route("/valves")
def valves():
    if isAdmin(): return db["valves"].query("select id, name, isPump, lat, lng, waterVolume, RH, temp, kgFertilizer from valves") | deref() | aS(json.dumps)
    gv = db["groupValves"].lookup(groupId=authGuard() | filt(lambda x: session["userId"] in x, 1) | cut(0) | item())
    return "[]" if not gv else [[v.id, v.name, v.isPump, v.lat, v.lng] for v in db["valves"][gv.valveIds.split(";") | filt("x") | apply(int) | aS(set) | aS(list) | deref()]] | deref() | aS(json.dumps)
@app.route("/timeouts")
def timeouts(): return db["timeouts"].query("select valveId, timeout from timeouts") | deref()
@app.route("/valvesTable")
def valvesTable(isAdmin_=True): _ui = valves() | aS(json.loads) | sortF(lambda x: x.strip("#").split("-") | apply(int) | ~aS(lambda x,y: x*100+y), 1) | (toJsFunc("van") | grep("${van}", col=1) | viz.Table(["idx", ui.trans("Valve", "Van"), ui.trans("Is pump?", "Là bơm?"), ui.trans("Latitude", "Vĩ tuyến"), ui.trans("Longitude", "Kinh tuyến")], onclickFName="selectValve", selectable=True, selectCallback="valvesTableSelectCb", height=350, **({"ondeleteFName":"deleteValve", "oneditFName":"editValve"} if isAdmin_ else {})) | executeScriptTags()) | op().interface() | toHtml(); return f"""<div id="div_valvesTable">{_ui}</div>
<style>
    #div_valvesTable tr:first-child {{ background: black !important; color: white; }}
</style>
<script>
    selectedValve = null; selectedValveTd = null;
    async function deleteValve(row, i, e) {{
        if (i < 0) return;
        if (!await confirm(`{ui.trans('Do you really want to remove valve', 'Bạn có thật sự muốn xoá van')} '${{row[1]}}'{ui.trans('', ' không')}? {ui.trans('This action cannot be undone', 'Một khi đã xoá sẽ không lấy lại được')}`)) return "dont_delete";
        await wrapToastReq(fetch(`/deleteValve/${{row[0]}}`));
    }}
    async function selectValve(row, i, e) {{
        console.log("selectValve", selectedValveTd, row, i, e)
        if (selectedValveTd) {{
            (async () => {{
                console.log("changed colors", selectedValveTd);
                selectedValveTd.parentElement.style.background = "";
                selectedValveTd.parentElement.style.color = "";
            }})();
        }}
        if (i < 0) return; window.selectedValve = row[0]; handleClick(row[0]); map.setView([row[3], row[4]], 18);
        window.selectedValveTd = e.srcElement;
        e.srcElement.parentElement.style.background = "#73bc4c";
        e.srcElement.parentElement.style.color = "white";
    }}
    async function editValve(row, row2, i, e) {{
        if (row[0] != row2[0]) throw new Error("{ui.trans("Valve id can't change", "Van id không thể thay đổi")}");
        await wrapToastReq(fetch(`/editValve`, {{ method: "POST", headers: {{ "Content-Type": "application/json" }}, body: JSON.stringify({{ id: parseInt(row2[0]), name: row2[1], isPump: row2[2].toLowerCase().startsWith("t"), lat: parseFloat(row2[3]), lng: parseFloat(row2[4]) }}) }}));
    }}
</script>"""
@app.route("/editValve", methods=["POST"], guard=adminGuard)
def editValve(): js = request.json; db["valves"][int(js["id"])] = {"name": js["name"], "isPump": bool(js["isPump"]), "lat": float(js["lat"]), "lng": float(js["lng"])}; print(db["valves"][int(js["id"])]); return "ok"
@app.route("/newValve", methods=["POST"], guard=adminGuard)
def newValve(): js = request.json; name = "#" + js["name"].strip("#"); lat = float(js["lat"]); lng = float(js["lng"]); db["valves"].insert(name=name, lat=lat, lng=lng); return "ok"
@app.route("/deleteValve/<int:idx>", guard=adminGuard)
def deleteValve(idx): del db["valves"][idx]; raise flask.SuccessException(ui.trans("Deleted successfully", "Xoá thành công"))
def fragment_valvesTable(isAdmin_=True):
    s1 = f"""
<div style="width: 100%; display: flex; flex-direction: row; flex-wrap: wrap; margin-top: 12px">
    <div style="display: flex; flex-direction: row; margin-bottom: 8px">
        <input type="text" id="lat" placeholder="{ui.trans("Latitude", "Vĩ tuyến")}" class="input input-bordered" style="flex: 1; max-width: 130px" />
        <input type="text" id="lng" placeholder="{ui.trans("Longitude", "Kinh tuyến")}" class="input input-bordered" style="flex: 1; max-width: 130px" />
    </div>
    <div style="display: flex; flex-direction: row">
        <input type="text" id="name" placeholder="{ui.trans("Valve name, eg '40-3'", "Tên van, vd '40-3'")}" class="input input-bordered" style="flex: 1; max-width: 200px" />
        <button class="btn" style="margin-left: 8px" onclick="newValve()">{ui.trans("Add valve", "Thêm van")}</button>
    </div>
</div>

"""
    return f"""<h2>{ui.trans('List of valves', 'Tất cả van')}</h2><div id="valvesTable" style="margin-top: 16px">{valvesTable(isAdmin_)}</div>{s1 if isAdmin_ else ''}
<script>
    async function refreshValvesTable() {{ dynamicLoad("#valvesTable", "/valvesTable"); }}
    async function newValve() {{
        name = document.querySelector("#name").value; lat  = document.querySelector("#lat").value; lng  = document.querySelector("#lng").value;
        await wrapToastReq(fetch("/newValve", {{ method: "POST", headers: {{ "Content-Type": "application/json" }}, body: JSON.stringify({{ name, lat, lng }}) }}));
        refreshValvesTable();
    }}
</script>"""

def getAlloIr():
    gs = cdb["groups"].select("select * from groups where app = 'ecopark' and name != 'ecopark_admin' and app = 'ecopark'")
    actualGs = db["groupValves"].select("select * from groupValves where groupId in %s", tuple([g.id for g in gs]))
    missingGs = gs | op().id.all() | ~inSet(actualGs | op().groupId.all() | deref()) | deref()
    for gId in missingGs: db["groupValves"].insert(groupId=gId, valveIds="")
    if len(missingGs): actualGs = db["groupValves"].select("select * from groupValves where groupId in %s", tuple([g.id for g in gs]))
    return [gs | apply(lambda g: [g.id, [g.name, len(g.userIds)]]), actualGs | apply(lambda g: [g.groupId, [g.valveIds]])] | joinSt() | groupBy(0, True) | apply(joinSt(2), 1) | ~apply(lambda x,y: [x,*y]) | deref()
def fragment_groups(): ir = getAlloIr(); ui1 = ir | apply(op().split(";") | filt("x") | shape(0), 3) | viz.Table(["idx", ui.trans("Group name", "Tên nhóm"), ui.trans("#Users", "#Người dùng"), ui.trans("#Valves", "#Van")], onclickFName="selectGroup", selectable=True); return f"""
<div style="display: flex; flex-direction: row; align-items: center">
    <h2>{ui.trans('Groups', 'Nhóm')}</h2>
    <button class="btn" onclick="window.location = 'https://auth.aigu.vn/groups/ecopark/{k1lib.aes_encrypt(json.dumps({"ownerGroupId": 2}).encode())}'" style="margin-left: 12px">{ui.trans("Group management", "Quản lý nhóm")}</button>
</div><div style="overflow-x: auto">{ui1}</div>
<button class="btn" onclick="addValveToGroup()" style="margin-top: 8px">{ui.trans("Add valve to group", "Thêm van vào nhóm")}</button>
<script>
    selectedGroup = null
    function selectGroup(row, i, e) {{ if (i < 0) return; window.selectedGroup = row[0]; console.log(row); dynamicLoad("#fragment_group", `/_fragment_group/${{row[0]}}`); }}
    async function addValveToGroup() {{
        if (!selectedGroup) {{ addToast("{ui.trans("Please select a group first", "Hãy chọn 1 nhóm trước")}"); return; }}
        if (!selectedValve) {{ addToast("{ui.trans("Please select a valve first", "Hãy chọn 1 van trước")}"); return; }}
        console.log(selectedGroup, selectedValve);
        await wrapToastReq(fetch(`/_addValveToGroup/${{selectedGroup}}/${{selectedValve}}`));
        dynamicLoad("#fragment_group", `/_fragment_group/${{selectedGroup}}`);
    }}
</script>"""
@app.route("/_addValveToGroup/<groupId>/<valveId>", guard=adminGuard)
def addValveToGroup(groupId, valveId): gv = db["groupValves"].lookup(groupId=int(groupId)); gv.valveIds = [*gv.valveIds.split(";") | filt("x") | apply(int), int(valveId)] | aS(set) | join(";"); return "ok"
@app.route("/_fragment_group/<groupId>", guard=adminGuard)
def fragment_group(groupId):
    ir = getAlloIr(); group = cdb["groups"][int(groupId)]
    valves = db["valves"][ir | filt(f"x == {group.id}", 0) | cut(3) | item() | op().split(";") | filt("x") | apply(int) | deref()]
    ui1 = valves | apply(lambda x: [x.id, x.name]) | sortF(lambda x: x.strip("#").split("-") | apply(int) | ~aS(lambda x,y: x*100+y), 1) | viz.Table(["idx", ui.trans("Valve", "Van")], ondeleteFName="deleteValveFromGroup", height=300); return f"""
<h2>{ui.trans(f'Valves group "{group.name}" can control', f'Van nhóm "{group.name}" điều khiển được')}</h2>
{ui1}<script>async function deleteValveFromGroup(row, i, e) {{ await wrapToastReq(fetch(`/_deleteValveFromGroup/{group.id}/${{row[0]}}`)); }}</script>"""
@app.route("/_deleteValveFromGroup/<groupId>/<valveId>", guard=adminGuard)
def deleteValveFromGroup(groupId, valveId): gv = db["groupValves"].lookup(groupId=int(groupId)); gv.valveIds = gv.valveIds.split(";") | filt("x") | apply(int) | filt(op()!=int(valveId)) | join(";"); return "ok"

app.run(host="0.0.0.0", port=80)




