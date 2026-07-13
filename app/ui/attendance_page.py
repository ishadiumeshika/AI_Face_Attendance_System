import streamlit as st
import pandas as pd

from app.database.attendance import get_attendance_history


def attendance_page():

    st.title("📋 Attendance History")


    records = get_attendance_history()


    if not records:

        st.info("No attendance records found")
        return



    data = []


    for row in records:

        data.append(
            {
                "Name": row["name"],
                "Date": row["date"],
                "Time": row["time"]
            }
        )


    df = pd.DataFrame(data)



    search = st.text_input(
        "🔍 Search name"
    )


    if search:

        df = df[
            df["Name"]
            .str.contains(
                search,
                case=False
            )
        ]



    st.dataframe(
        df,
        use_container_width=True
    )


    csv = df.to_csv(
        index=False
    )


    st.download_button(
        "📥 Export CSV",
        csv,
        "attendance.csv",
        "text/csv"
    )