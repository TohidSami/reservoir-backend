from flask import Blueprint, jsonify, send_file
from sqlalchemy import text
import pandas as pd
import matplotlib.pyplot as plt
import io
import numpy as np
from app.database import engine


plot_bp = Blueprint('plots', __name__)

@plot_bp.route("/api/wells/<int:well_id>/plot")
def get_plot(well_id):
    try:
        sql = text("""
            SELECT report_date, oil_rate, gas_rate, water_rate 
            FROM production_data 
            WHERE well_id=:id ORDER BY report_date ASC
        """)
        
        with engine.connect() as connection:
            df = pd.read_sql(sql, connection, params={"id": well_id})
            
        if df.empty:
            return jsonify({"error": "No data to plot"}), 404

       
        df.set_index('report_date', inplace=True)
        df['gor'] = (df['gas_rate'] * 1000) / df['oil_rate'].replace(0, 0.001)
        total_liquid = df['oil_rate'] + df['water_rate']
        df['wc'] = (df['water_rate'] / total_liquid.replace(0, 0.001)) * 100
        df.fillna(0, inplace=True)

        
        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 8), sharex=True)
        
        ax1.plot(df.index, df['oil_rate'], color='green', label='Oil Rate')
        ax1.set_ylabel('Oil (bbl/d)')
        ax1.legend(loc='upper right')
        ax1.grid(True)
        ax1.set_title(f'Well {well_id} Performance')

        ax2.plot(df.index, df['gor'], color='red', label='GOR')
        ax2.set_ylabel('GOR (scf/bbl)')
        ax2.legend(loc='upper right')
        ax2.grid(True)

        ax3.plot(df.index, df['wc'], color='blue', label='Water Cut')
        ax3.set_ylabel('WC (%)')
        ax3.legend(loc='upper right')
        ax3.grid(True)

        plt.tight_layout()

       
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        plt.close(fig) 

        return send_file(buf, mimetype='image/png', download_name=f'well_{well_id}.png')

    except Exception as e:
        return jsonify({"error": str(e)}), 500