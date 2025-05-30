import streamlit as st
import pandas as pd

st.title("共通列を使って複数CSVファイルを結合するアプリ")

# CSVファイルのアップロード
uploaded_files = st.file_uploader(
    "CSVファイルを複数選択してください（共通列だけで結合されます）",
    type="csv",
    accept_multiple_files=True
)

if uploaded_files:
    dfs = []
    for uploaded_file in uploaded_files:
        try:
            df = pd.read_csv(uploaded_file)
            dfs.append(df)
            st.success(f"{uploaded_file.name} を読み込みました（{df.shape[0]}行 × {df.shape[1]}列）")
        except Exception as e:
            st.error(f"{uploaded_file.name} の読み込みに失敗しました: {e}")

    if len(dfs) >= 2:
        # 共通列を取得
        common_cols = set(dfs[0].columns)
        for df in dfs[1:]:
            common_cols &= set(df.columns)

        if common_cols:
            st.info(f"共通列: {sorted(common_cols)}")
            dfs_common = [df[list(common_cols)] for df in dfs]
            merged_df = pd.concat(dfs_common, ignore_index=True)
            st.write("✅ 結合結果プレビュー:")
            st.dataframe(merged_df)

            csv = merged_df.to_csv(index=False)
            st.download_button(
                label="📥 CSVとしてダウンロード",
                data=csv,
                file_name="merged_common_columns.csv",
                mime="text/csv"
            )
        else:
            st.error("アップロードされたファイルに共通の列がありません。")
else:
    st.info("CSVファイルをアップロードしてください。共通列が自動的に判定されます。")
