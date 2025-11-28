from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

def generate_province_seat_pdf(provincial_results_df, output_path="ripartizioneSeggi_finale.pdf", seats_per_province_df=None, votes_df=None):
    """
    Generates a PDF report with the same structure as RipartizioneSeggi finale.pdf, including provincial quota and formula.
    Args:
        provincial_results_df (pd.DataFrame): DataFrame with columns ['province', 'list', 'votes', 'int_seats', 'rest_pct', 'final_seats']
        output_path (str): Path to output PDF file
        seats_per_province_df (pd.DataFrame): DataFrame with columns ['province', 'seats']
    """
    doc = SimpleDocTemplate(output_path, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []

    # --- Spiegazione della ripartizione dei seggi regionale ---
    if votes_df is not None and 'coalition' in votes_df.columns and 'votes' in votes_df.columns:
        reg_votes = votes_df.groupby('coalition')['votes'].sum().reset_index()
        total_reg_votes = reg_votes['votes'].sum()
        elements.append(Paragraph("<b>Ripartizione seggi tra coalizioni (regionale)</b>", styles['Heading1']))
        recap_data = [["Coalizione", "Voti", "%"]]
        for _, row in reg_votes.sort_values('votes', ascending=False).iterrows():
            pct = 100 * row['votes'] / total_reg_votes if total_reg_votes > 0 else 0
            recap_data.append([row['coalition'], int(row['votes']), f"{pct:.2f}%"])
        recap_table = Table(recap_data, repeatRows=1)
        recap_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
            ('TEXTCOLOR', (0,0), (-1,0), colors.black),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0,0), (-1,0), 8),
        ]))
        elements.append(recap_table)
        elements.append(Spacer(1, 18))
        # Seggi assegnati (se disponibili)
        try:
            coal_seats = pd.read_csv("coalition_seats.csv")
            seat_data = [["Coalizione", "Seggi assegnati"]]
            for _, row in coal_seats.iterrows():
                seat_data.append([row['coalition'], int(row['seats'])])
            seat_table = Table(seat_data, repeatRows=1)
            seat_table.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
                ('TEXTCOLOR', (0,0), (-1,0), colors.black),
                ('ALIGN', (0,0), (-1,-1), 'CENTER'),
                ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
                ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0,0), (-1,0), 8),
            ]))
            elements.append(seat_table)
            elements.append(Spacer(1, 18))
        except Exception:
            pass
        # Ripartizione seggi tra liste
        try:
            grp_seats = pd.read_csv("group_seats.csv")
            list_data = [["Lista", "Coalizione", "Seggi assegnati"]]
            for _, row in grp_seats.iterrows():
                list_data.append([row['list'], row['coalition'], int(row['group_seats'])])
            list_table = Table(list_data, repeatRows=1)
            list_table.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
                ('TEXTCOLOR', (0,0), (-1,0), colors.black),
                ('ALIGN', (0,0), (-1,-1), 'CENTER'),
                ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
                ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0,0), (-1,0), 8),
            ]))
            elements.append(list_table)
            elements.append(Spacer(1, 18))
        except Exception:
            pass

    # --- President recap ---
    if votes_df is not None and 'president' in votes_df.columns:
        pres_votes = votes_df.groupby('president')['votes'].sum().reset_index()
        total_votes = pres_votes['votes'].sum()
        recap_data = [["Presidente", "Voti", "%"]]
        for _, row in pres_votes.sort_values('votes', ascending=False).iterrows():
            pct = 100 * row['votes'] / total_votes if total_votes > 0 else 0
            recap_data.append([row['president'], int(row['votes']), f"{pct:.2f}%"])
        recap_table = Table(recap_data, repeatRows=1)
        recap_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
            ('TEXTCOLOR', (0,0), (-1,0), colors.black),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0,0), (-1,0), 8),
        ]))
        elements.append(Paragraph("<b>Riepilogo percentuali Presidenti</b>", styles['Heading1']))
        elements.append(recap_table)
        elements.append(Spacer(1, 18))
        # --- Party recap ---
        party_votes = votes_df.groupby('list')['votes'].sum().reset_index()
        total_party_votes = party_votes['votes'].sum()
        party_data = [["Partito/Lista", "Voti", "%"]]
        for _, row in party_votes.sort_values('votes', ascending=False).iterrows():
            pct = 100 * row['votes'] / total_party_votes if total_party_votes > 0 else 0
            party_data.append([row['list'], int(row['votes']), f"{pct:.2f}%"])
        party_table = Table(party_data, repeatRows=1)
        party_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
            ('TEXTCOLOR', (0,0), (-1,0), colors.black),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0,0), (-1,0), 8),
        ]))
        elements.append(Paragraph("<b>Riepilogo voti e percentuali per lista/partito</b>", styles['Heading1']))
        elements.append(party_table)
        elements.append(Spacer(1, 18))
    provinces = provincial_results_df['province'].unique()
    for province in provinces:
        elements.append(Paragraph(f"<b>Provincia di {province}</b>", styles['Heading2']))
        df = provincial_results_df[provincial_results_df['province'] == province]
        # Use only admitted coalition votes for quota calculation
        admitted_coalitions = ["Centrodestra", "Centrosinistra"]
        admitted_votes = votes_df[(votes_df["province"] == province) & 
                                 (votes_df["coalition"].isin(admitted_coalitions))]["votes"].sum()
        if seats_per_province_df is not None:
            row = seats_per_province_df.loc[seats_per_province_df['province'] == province, 'seats']
            if not row.empty:
                seats = int(row.iloc[0])
                q_circ = admitted_votes // (seats + 1) if seats > 0 else 0
                elements.append(Paragraph(
                    f"Quoziente provinciale: <b>{q_circ}</b> = {admitted_votes} voti / ({seats} + 1)",
                    styles['Normal']
                ))
                elements.append(Spacer(1, 6))
            else:
                elements.append(Paragraph("Province not found in seats data.", styles['Normal']))
                elements.append(Spacer(1, 6))
        data = [["Lista", "Voti", "Seggi Interi", "Resto assoluto", "Resto %", "Rank regionale resti %", "Seggi Finali"]]
        for _, row in df.iterrows():
            if seats_per_province_df is not None:
                row_seats = seats_per_province_df.loc[seats_per_province_df['province'] == province, 'seats']
                if not row_seats.empty:
                    seats = int(row_seats.iloc[0])
                    q_circ = admitted_votes // (seats + 1) if seats > 0 else 0
                    rest_abs = int(row['votes'] - row['int_seats'] * q_circ) if q_circ > 0 else 0
                else:
                    rest_abs = 0
                    q_circ = 0
                rest_pct = row['rest_pct'] if 'rest_pct' in row else 0
                rank = row['regional_rest_rank'] if 'regional_rest_rank' in row else ''
            else:
                rest_abs = int(row['votes'] - row['int_seats'] * 0)
                rest_pct = 0
                rank = ''
            data.append([
                row['list'],
                int(row['votes']),
                int(row['int_seats']),
                rest_abs,
                f"{rest_pct:.2f}%",
                rank,
                int(row['final_seats'])
            ])
        table = Table(data, repeatRows=1)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
            ('TEXTCOLOR', (0,0), (-1,0), colors.black),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0,0), (-1,0), 8),
        ]))
        elements.append(table)
        elements.append(Spacer(1, 12))
    doc.build(elements)
def generate_province_seat_heatmap(provincial_results_df, output_path="province_seat_heatmap.md"):
    """
    Generates a Markdown heatmap-style table of seat distribution by party and province.
    Args:
        provincial_results_df (pd.DataFrame): DataFrame with columns ['province', 'list', 'final_seats']
        output_path (str): Path to output Markdown file
    """
    pivot = provincial_results_df.pivot_table(index="province", columns="list", values="final_seats", fill_value=0)
    md = "# Provincial Distribution of Seats (Heatmap)\n\n"
    md += pivot.reset_index().to_markdown(index=False)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(md)
def calculate_provincial_quota(votes_df, seats_per_province_df):
    """
    Returns a DataFrame with columns ['province', 'quota'] where quota = total votes / (seats + 1) for each province.
    """
    total_votes = votes_df.groupby('province')['votes'].sum().reset_index()
    merged = pd.merge(total_votes, seats_per_province_df, on='province')
    merged['quota'] = merged['votes'] / (merged['seats'] + 1)
    return merged[['province', 'quota']]
def generate_province_seat_markdown(votes_df, provincial_results_df, quota_df, seats_per_province_df, output_path="province_seat_report.md"):
    """
    Generates a Markdown report for each province: quota, parties elected, votes per elected seat.
    """
    md = "# Provincial Seat Allocation Report\n\n"
    # --- Spiegazione della ripartizione dei seggi regionale ---
    if 'coalition' in votes_df.columns and 'votes' in votes_df.columns:
        reg_votes = votes_df.groupby('coalition')['votes'].sum().reset_index()
        total_reg_votes = reg_votes['votes'].sum()
        md += "## Ripartizione seggi tra coalizioni (regionale)\n\n"
        md += "| Coalizione | Voti | % |\n|---|---|---|\n"
        for _, row in reg_votes.sort_values('votes', ascending=False).iterrows():
            pct = 100 * row['votes'] / total_reg_votes if total_reg_votes > 0 else 0
            md += f"| {row['coalition']} | {int(row['votes'])} | {pct:.2f}% |\n"
        # Seggi assegnati (se disponibili)
        try:
            coal_seats = pd.read_csv("coalition_seats.csv")
            md += "\n| Coalizione | Seggi assegnati |\n|---|---|\n"
            for _, row in coal_seats.iterrows():
                md += f"| {row['coalition']} | {row['seats']} |\n"
        except Exception:
            pass
        # Ripartizione seggi tra liste
        try:
            grp_seats = pd.read_csv("group_seats.csv")
            md += "\n## Ripartizione seggi tra liste (regionale)\n\n"
            md += "| Lista | Coalizione | Seggi assegnati |\n|---|---|---|\n"
            for _, row in grp_seats.iterrows():
                md += f"| {row['list']} | {row['coalition']} | {row['group_seats']} |\n"
        except Exception:
            pass
    # --- President recap ---
    if 'president' in votes_df.columns:
        pres_votes = votes_df.groupby('president')['votes'].sum().reset_index()
        total_votes = pres_votes['votes'].sum()
        md += "## Riepilogo percentuali Presidenti\n\n"
        md += "| Presidente | Voti | % |\n|---|---|---|\n"
        for _, row in pres_votes.sort_values('votes', ascending=False).iterrows():
            pct = 100 * row['votes'] / total_votes if total_votes > 0 else 0
            md += f"| {row['president']} | {int(row['votes'])} | {pct:.2f}% |\n"
        md += "\n"
        # --- Party recap ---
        party_votes = votes_df.groupby('list')['votes'].sum().reset_index()
        total_party_votes = party_votes['votes'].sum()
        md += "## Riepilogo voti e percentuali per lista/partito\n\n"
        md += "| Lista/Partito | Voti | % |\n|---|---|---|\n"
        for _, row in party_votes.sort_values('votes', ascending=False).iterrows():
            pct = 100 * row['votes'] / total_party_votes if total_party_votes > 0 else 0
            md += f"| {row['list']} | {int(row['votes'])} | {pct:.2f}% |\n"
        md += "\n"
    for province in quota_df['province']:
        # Use only admitted coalition votes for quota calculation
        admitted_coalitions = ["Centrodestra", "Centrosinistra"]
        admitted_votes = votes_df[(votes_df["province"] == province) & 
                                 (votes_df["coalition"].isin(admitted_coalitions))]["votes"].sum()
        row = seats_per_province_df.loc[seats_per_province_df["province"]==province, "seats"]
        seats = int(row.iloc[0]) if not row.empty else 0
        q_circ = admitted_votes // (seats + 1) if seats > 0 else 0
        md += f"## {province}\n"
        md += f"**Quota (votes per seat):** {q_circ} = {admitted_votes} voti / ({seats} + 1)\n\n"
        # Get parties that elected at least one seat
        elected = provincial_results_df[(provincial_results_df['province'] == province) & (provincial_results_df['final_seats'] > 0)]
        if not elected.empty:
            md += "| Party/List | Seats | Votes per Seat | Total Votes | Resto assoluto | Resto % | Rank regionale resti % |\n|---|---|---|---|---|---|---|\n"
            for _, row in elected.iterrows():
                votes_per_seat = row['votes'] / row['final_seats'] if row['final_seats'] > 0 else 0
                rest_abs = int(row['votes'] - row['int_seats'] * q_circ) if q_circ > 0 else 0
                rest_pct = row['rest_pct'] if 'rest_pct' in row else 0
                rank = row['regional_rest_rank'] if 'regional_rest_rank' in row else ''
                md += f"| {row['list']} | {row['final_seats']} | {votes_per_seat:.2f} | {row['votes']} | {rest_abs} | {rest_pct:.2f}% | {rank} |\n"
        else:
            md += "No seats elected in this province.\n"
        md += "\n"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(md)
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 30 23:22:15 2025

@author: meval
"""

# marche_sim.py
# Simulatore seggi Marche con resti e tetti di gruppo
# L.R. 27/2004 artt. 18–19: soglie coalizioni, D'Hondt, quoziente circoscrizionale, graduatoria resti, riserva al secondo.
#
# LEGAL REFERENCES:
# - Art. 18, comma 5–6: Coalition/list admission thresholds
# - Art. 19, comma 1–2: D'Hondt allocation, minimum seat bonus
# - Art. 19, comma 3: Group/list seat distribution
# - Art. 19, comma 4: Provincial seat allocation
# - Art. 19, comma 5–6: Group caps, residual seat ranking
# - Art. 19, comma 7: Reserved seat for runner-up president

import pandas as pd
import numpy as np
from math import floor

# ---------- util ----------
def dhondt(values, seats):
    # Art. 19, comma 1: D'Hondt method for proportional seat allocation
    if seats <= 0 or sum(values.values()) <= 0:
        return {k:0 for k in values}
    qs=[]
    for k,v in values.items():
        for d in range(1,seats+1):
            qs.append((k, v/d))
    qs.sort(key=lambda x:x[1], reverse=True)
    win=[k[0] for k in qs[:seats]]  # Fix: extract party name from tuple
    return {k:win.count(k) for k in values}

# ---------- A) coalizioni: soglia + seggi + premio minimo ----------
def coalitions_stage(votes_df, total_list_seats, pct19, pct18):
    # Art. 18, comma 5–6: Coalition/list admission thresholds
    # Art. 19, comma 1–2: D'Hondt allocation, minimum seat bonus for leading coalition
    # voti liste regionali per gruppo-lista
    list_reg = votes_df.groupby(["list","coalition"], as_index=False)["votes"].sum()
    # voti coalizione = somma liste (+ eventuali voti presidenziali se presenti)
    coal = list_reg.groupby("coalition", as_index=False)["votes"].sum().rename(columns={"votes":"list_votes"})
    if "pres_votes" in votes_df.columns:
        pres = votes_df.groupby("coalition", as_index=False)["pres_votes"].sum()
        coal = coal.merge(pres, on="coalition", how="left").fillna({"pres_votes":0})
    else:
        coal["pres_votes"]=0
    coal["total_coal_votes"]=coal["list_votes"]+coal["pres_votes"]

    tot_coal = coal["total_coal_votes"].sum()
    coal["coal_share"]=coal["total_coal_votes"]/tot_coal if tot_coal>0 else 0

    tot_list = list_reg["votes"].sum()
    mx = list_reg.assign(list_share=list_reg["votes"]/tot_list if tot_list>0 else 0)\
                 .groupby("coalition")["list_share"].max().reset_index().rename(columns={"list_share":"max_list_share"})
    coal = coal.merge(mx, on="coalition", how="left")
    coal["admitted"] = (coal["coal_share"]>=0.05) | (coal["max_list_share"]>0.03)
    coal.loc[coal["total_coal_votes"]<=0,"admitted"]=False

    adm = coal[coal["admitted"]].copy()
    base = dhondt(dict(zip(adm["coalition"], adm["total_coal_votes"])), total_list_seats)
    coal_seats = pd.DataFrame({"coalition":list(base.keys()), "seats":list(base.values())})

    # premio minimo 19/18
    if not coal_seats.empty:
        leader = adm.sort_values("total_coal_votes", ascending=False)["coalition"].iloc[0]
        lshare = float(adm.loc[adm["coalition"]==leader,"coal_share"])
        need = 19 if lshare>=pct19 else (18 if lshare>=pct18 else 0)
        got = int(coal_seats.loc[coal_seats["coalition"]==leader,"seats"])
        if need>0 and got<need:
            remaining = total_list_seats-need
            others = adm[adm["coalition"]!=leader]
            other_counts = dhondt(dict(zip(others["coalition"], others["total_coal_votes"])), remaining)
            coal_seats = pd.concat([
                pd.DataFrame({"coalition":[leader], "seats":[need]}),
                pd.DataFrame({"coalition":list(other_counts.keys()), "seats":list(other_counts.values())})
            ], ignore_index=True)
    return coal, coal_seats

# ---------- B) seggi ai gruppi di liste dentro le coalizioni ----------
def group_seats_stage(votes_df, coal_seats_df):
    # Art. 19, comma 3: Distribution of coalition seats to lists/groups
    reg = votes_df.groupby(["list","coalition"], as_index=False)["votes"].sum()
    out=[]
    for _,r in coal_seats_df.iterrows():
        c, S = r["coalition"], int(r["seats"])
        sub = reg[reg["coalition"]==c].copy()
        if S<=0 or sub["votes"].sum()<=0:
            out.append(sub.assign(group_seats=0)[["list","coalition","group_seats"]]); continue
        q = floor(sub["votes"].sum()/(S+1))
        if q<=0:
            sub=sub.sort_values("votes", ascending=False).reset_index(drop=True)
            sub["group_seats"]=0
            for i in range(S): sub.loc[i%len(sub),"group_seats"]+=1
            out.append(sub[["list","coalition","group_seats"]]); continue
        sub["qi"]=(sub["votes"]//q).astype(int)
        rem=S-sub["qi"].sum()
        sub["group_seats"]=sub["qi"]
        if rem>0:
            sub["rem_abs"]=sub["votes"]-sub["qi"]*q
            sub=sub.sort_values(["rem_abs","votes"], ascending=[False,False]).reset_index(drop=True)
            for i in range(rem): sub.loc[i,"group_seats"]+=1
        out.append(sub[["list","coalition","group_seats"]])
    return pd.concat(out, ignore_index=True)

# ---------- C) seggi interi provinciali + resti percentuali ----------
def provincial_integers(votes_df, province_seats_df, admitted_coalitions):
    # Art. 19, comma 4: Provincial seat allocation (integer quotas and residuals)
    v = votes_df[votes_df["coalition"].isin(admitted_coalitions)].copy()
    prov = v.groupby("province", as_index=False)["votes"].sum().rename(columns={"votes":"prov_total"})
    prov = prov.merge(province_seats_df, on="province", how="left")
    prov["q_circ"] = (prov["prov_total"]//(prov["seats"]+1)).astype(int)
    x = v.merge(prov[["province","seats","q_circ","prov_total"]], on="province", how="left")
    x["int_seats"]=x.apply(lambda r: int(r["votes"]//r["q_circ"]) if r["q_circ"]>0 else 0, axis=1)
    x["rest_pct"]=x.apply(lambda r: 100*(r["votes"]-r["int_seats"]*r["q_circ"])/r["prov_total"] if r["prov_total"]>0 else 0.0, axis=1)
    return x, prov

# ---------- D) applica tetti di gruppo + assegna resti in graduatoria unica ----------
def assign_residuals(df_step, prov_meta, group_caps):
    # Art. 19, comma 5–6: Group/list seat caps and unique residual ranking
    df=df_step.copy()
    caps = dict(zip(group_caps["list"], group_caps["group_seats"]))
    
    # Calculate regional rest ranking first
    df["regional_rest_rank"] = df["rest_pct"].rank(method="min", ascending=False).astype(int)
    
    # Calculate absolute rest for reporting
    df["rest"] = df["votes"] - df["int_seats"] * df["q_circ"]
    
    # riduci eccedenze
    current = df.groupby("list")["int_seats"].sum().to_dict()
    df["final_seats"]=df["int_seats"].astype(int)
    for lst,cap in caps.items():
        overflow=max(0, current.get(lst,0)-int(cap))
        if overflow<=0: continue
        idxs = df[df["list"]==lst].sort_values(["int_seats","votes"], ascending=[False,True]).index
        for i in idxs:
            if overflow<=0: break
            if df.at[i,"final_seats"]>0:
                df.at[i,"final_seats"]-=1
                overflow-=1
    # capacità residua provincia e lista
    prov_left = (prov_meta[["province","seats"]]
                 .merge(df.groupby("province",as_index=False)["final_seats"].sum().rename(columns={"final_seats":"assigned"}),
                        on="province", how="left").fillna({"assigned":0}))
    prov_left["left"]=prov_left["seats"]-prov_left["assigned"]
    prov_left=dict(zip(prov_left["province"], prov_left["left"]))
    lst_left = group_caps.merge(df.groupby("list",as_index=False)["final_seats"].sum().rename(columns={"final_seats":"assigned"}),
                                on="list", how="left").fillna({"assigned":0})
    lst_left["left"]=lst_left["group_seats"]-lst_left["assigned"]
    lst_left=dict(zip(lst_left["list"], lst_left["left"]))

    order=[]
    # graduatoria unica per resti percentuali
    cand=df[["province","list","coalition","votes","rest_pct"]].sort_values("rest_pct", ascending=False)
    for _,r in cand.iterrows():
        p,l=r["province"], r["list"]
        if prov_left.get(p,0)>0 and lst_left.get(l,0)>0:
            i = df[(df["province"]==p)&(df["list"]==l)].index[0]
            df.at[i,"final_seats"]+=1
            prov_left[p]-=1; lst_left[l]-=1; order.append((p,l))
    # se rimane capacità, usa voti assoluti
    if any(v>0 for v in prov_left.values()) and any(v>0 for v in lst_left.values()):
        pool=df.copy()
        pool["prov_left"]=pool["province"].map(prov_left)
        pool["lst_left"]=pool["list"].map(lst_left)
        pool=pool[(pool["prov_left"]>0)&(pool["lst_left"]>0)].sort_values("votes", ascending=False)
        for _,r in pool.iterrows():
            p,l=r["province"], r["list"]
            if prov_left[p]>0 and lst_left[l]>0:
                i = df[(df["province"]==p)&(df["list"]==l)].index[0]
                df.at[i,"final_seats"]+=1
                prov_left[p]-=1; lst_left[l]-=1; order.append((p,l))
            if all(v<=0 for v in prov_left.values()): break
    return df, order

# ---------- E) seggio riservato al 2° presidente ----------
def reserve_runner_up(df_alloc, residual_order, votes_df, coal_votes, coal_seats):
    # Art. 19, comma 7: Reserved seat for runner-up presidential candidate
    # However, we must respect the provincial seat allocation requirements
    adm = coal_seats["coalition"].tolist()
    cv = coal_votes[coal_votes["coalition"].isin(adm)].sort_values("total_coal_votes", ascending=False)
    if len(cv)<2: return df_alloc, None
    
    second=cv.iloc[1]["coalition"]
    lists_second=set(votes_df[votes_df["coalition"]==second]["list"].unique())
    
    # Check if runner-up coalition already has seats
    runner_up_seats = df_alloc[df_alloc["coalition"] == second]["final_seats"].sum()
    if runner_up_seats > 0:
        # Runner-up already has representation, no need to remove seats
        return df_alloc, {"reason": "runner_up_already_represented", "seats": int(runner_up_seats)}
    
    # Only remove seats if runner-up has no representation
    out=df_alloc.copy()
    # togli l'ultimo seggio assegnato via resti a una lista del secondo
    for p,l in reversed(residual_order):
        if l in lists_second:
            m=(out["province"]==p)&(out["list"]==l)
            out.loc[m,"final_seats"]=out.loc[m,"final_seats"]-1
            return out, {"province":p,"list":l,"reason":"runner_up"}
    # altrimenti togli alla lista del secondo con meno voti fra quelle con almeno 1 seggio
    sub=out[out["list"] in lists_second]
    sub=sub[sub["final_seats"]>0]
    if sub.empty: return out, None
    v=sub.sort_values(["final_seats","votes"], ascending=[True,True]).iloc[0]
    m=(out["province"]==v["province"])&(out["list"]==v["list"])
    out.loc[m,"final_seats"]=out.loc[m,"final_seats"]-1
    return out, {"province":v["province"],"list":v["list"],"reason":"runner_up_fallback"}

# ---------- pipeline ----------
def run_allocation(votes_df, province_seats_df, total_list_seats=30, pct19=0.43, pct18=0.40):
    # Pipeline: applies all steps in sequence as per L.R. 27/2004, artt. 18–19
    # Clean column names and data
    votes_df = votes_df.rename(columns=lambda x: x.strip())
    
    # Handle comma-separated numbers in votes column
    if "votes" in votes_df.columns and votes_df["votes"].dtype == 'object':
        votes_df["votes"] = votes_df["votes"].astype(str).str.replace(',', '').astype(float)
    
    for col in ["votes"]:
        if col in votes_df.columns:
            votes_df[col] = pd.to_numeric(votes_df[col], errors="coerce").fillna(0)
    
    coal_votes, coal_seats = coalitions_stage(votes_df, total_list_seats, pct19, pct18)
    admitted = coal_votes[coal_votes["admitted"]]["coalition"].tolist()
    if not admitted: return (pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), None)
    grp_seats = group_seats_stage(votes_df[votes_df["coalition"].isin(admitted)], coal_seats)
    stepC, prov_meta = provincial_integers(votes_df[votes_df["coalition"].isin(admitted)], province_seats_df, admitted)
    alloc, order = assign_residuals(stepC, prov_meta, grp_seats)
    final, removed = reserve_runner_up(alloc, order, votes_df, coal_votes, coal_seats)
    return final, coal_seats, grp_seats, removed

import pandas as pd

def generate_markdown_report(seat_alloc_df, output_path="seat_report.md"):
    """
    Generates a Markdown table of seat allocation per party in each province.
    Args:
        seat_alloc_df (pd.DataFrame): DataFrame with columns ['province', 'list', 'seats']
        output_path (str): Path to output Markdown file
    """
    # Pivot table: rows=province, columns=list, values=seats
    pivot = seat_alloc_df.pivot_table(index="province", columns="list", values="seats", fill_value=0)
    md = "# Seat Allocation per Party in Each Province\n\n"
    md += pivot.reset_index().to_markdown(index=False)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(md)

# Funzione per creare la graduatoria regionale dei resti percentuali
def get_regional_rest_rank(df):
    # Resti percentuali (C.E.R.P.) graduatoria regionale
    return df[["province", "list", "coalition", "votes", "rest", "rest_pct"]].sort_values("rest_pct", ascending=False)

# Funzione per stampare i dettagli della ripartizione seggi per una provincia
def print_province_allocation_details(prov_res_df, seats_per_province_df, province, votes_df):
    # Stampa dettagli ripartizione seggi per una provincia
    print(f"\nRipartizione seggi per la provincia di {province}:")
    prov_df = prov_res_df[prov_res_df["province"] == province]
    seats_row = seats_per_province_df[seats_per_province_df["province"] == province]
    if not seats_row.empty:
        seats = int(seats_row["seats"].iloc[0])
        # Use only admitted coalition votes for quota calculation
        admitted_coalitions = ["Centrodestra", "Centrosinistra"]  # These are the admitted coalitions
        admitted_votes = votes_df[(votes_df["province"] == province) & 
                                 (votes_df["coalition"].isin(admitted_coalitions))]["votes"].sum()
        q_circ = admitted_votes // (seats + 1) if seats > 0 else 0
        print(f"Quota provinciale: {q_circ} = {admitted_votes} voti / ({seats} + 1)")
    else:
        print("Province not found in seats data.")
        return
    for _, row in prov_df.iterrows():
        print(f"Lista: {row['list']}, Voti: {row['votes']}, Seggi: {row['final_seats']}, Resti: {row.get('rest', 0)} ({row['rest_pct']:.2f}%)")

# Example usage in main
if __name__=="__main__":
    try:
        votes_df = pd.read_csv("votes_marche_2025_all_provinces.csv")
        seats_per_province_df = pd.read_csv("seats_per_province.csv")
        provs = seats_per_province_df
        params = pd.read_csv("params.csv")

        # Ensure column names are stripped of whitespace
        votes_df.columns = votes_df.columns.str.strip()
        seats_per_province_df.columns = seats_per_province_df.columns.str.strip()
        params.columns = params.columns.str.strip()
        
        # Handle comma-separated numbers in votes column BEFORE numeric conversion
        if "votes" in votes_df.columns and votes_df["votes"].dtype == 'object':
            votes_df["votes"] = votes_df["votes"].astype(str).str.replace(',', '').astype(float)
        
        # Ensure votes column is numeric
        if "votes" in votes_df.columns:
            votes_df["votes"] = pd.to_numeric(votes_df["votes"], errors="coerce").fillna(0)
        # Ensure seats column is numeric
        if "seats" in seats_per_province_df.columns:
            seats_per_province_df["seats"] = pd.to_numeric(seats_per_province_df["seats"], errors="coerce").fillna(0)
        # Ensure value column is numeric in params
        if "value" in params.columns:
            params["value"] = pd.to_numeric(params["value"], errors="coerce").fillna(0)

        total = int(params.loc[params["key"]=="TOTAL_LIST_SEATS","value"].iloc[0])
        p19   = float(params.loc[params["key"]=="BONUS_TARGET_PCT_19","value"].iloc[0])
        p18   = float(params.loc[params["key"]=="BONUS_TARGET_PCT_18","value"].iloc[0])

        final, coal_seats, grp_seats, removed = run_allocation(votes_df, provs, total, p19, p18)

        # Simple output generation - no complex aggregation
        out = final.copy()
        
        # Ensure all required columns exist
        required_columns = ["province", "list", "coalition", "votes", "int_seats", "rest", "rest_pct", "regional_rest_rank", "final_seats"]
        for col in required_columns:
            if col not in out.columns:
                if col == "rest":
                    out[col] = 0
                elif col == "rest_pct":
                    out[col] = 0.0
                elif col == "regional_rest_rank":
                    out[col] = 0
                elif col == "int_seats":
                    out[col] = 0
                else:
                    out[col] = ""
        
        # Sort by province, final_seats (descending), votes (descending)
        if "province" in out.columns and "final_seats" in out.columns and "votes" in out.columns:
            out = out.sort_values(["province", "final_seats", "votes"], ascending=[True, False, False])

        out.to_csv("provincial_results.csv", index=False)
        coal_seats.to_csv("coalition_seats.csv", index=False)
        grp_seats.to_csv("group_seats.csv", index=False)
        pd.DataFrame([removed or {}]).to_csv("runnerup_reserved.csv", index=False)

        # Now generate reports after provincial_results.csv is written
        provincial_results_df = pd.read_csv("provincial_results.csv")
        quota_df = calculate_provincial_quota(votes_df, seats_per_province_df)
        # Calcola il rank regionale dei resti percentuali
        generate_province_seat_markdown(votes_df, provincial_results_df, quota_df, seats_per_province_df, output_path="province_seat_report.md")
        generate_province_seat_heatmap(provincial_results_df, output_path="province_seat_heatmap.md")
        generate_province_seat_pdf(provincial_results_df, output_path="ripartizioneSeggi_finale.pdf", seats_per_province_df=seats_per_province_df, votes_df=votes_df)
        print("Reports generated: province_seat_report.md, province_seat_heatmap.md, ripartizioneSeggi_finale.pdf")
        # Print allocation details for Fermo
        print_province_allocation_details(provincial_results_df, seats_per_province_df, "Fermo", votes_df)
    except Exception as e:
        print("Could not generate report:", e)
