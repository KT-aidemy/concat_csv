import streamlit as st
import pandas as pd
from io import StringIO

st.title("複数CSVファイルを結合するアプリ")

# アップロード
uploaded_files = st.file_uploader(
    "CSVファイルを複数選択してください", 
    type="csv", 
    accept_multiple_files=True
)

concat_axis = st.radio("結合方法を選んでください", ("縦に結合（行方向）", "横に結合（列方向）"))

# ファイルがアップロードされた場合
if uploaded_files:
    dfs = []
    for uploaded_file in uploaded_files:
        try:
            df = pd.read_csv(uploaded_file)
            dfs.append(df)
            st.success(f"{uploaded_file.name} を読み込みました（{df.shape[0]}行 × {df.shape[1]}列）")
        except Exception as e:
            st.error(f"{uploaded_file.name} の読み込みに失敗しました: {e}")

    # 結合処理
    if len(dfs) > 0:
        axis = 0 if concat_axis.startswith("縦") else 1
        try:
            merged_df = pd.concat(dfs, axis=axis, ignore_index=(axis == 0))
            st.write("✅ 結合結果プレビュー:")
            st.dataframe(merged_df)

            # ダウンロードリンク生成
            csv = merged_df.to_csv(index=False)
            st.download_button(
                label="📥 CSVとしてダウンロード",
                data=csv,
                file_name="merged_data.csv",
                mime="text/csv"
            )
        except Exception as e:
            st.error(f"結合処理中にエラーが発生しました: {e}")
else:
    st.info("CSVファイルを複数アップロードしてください。")
