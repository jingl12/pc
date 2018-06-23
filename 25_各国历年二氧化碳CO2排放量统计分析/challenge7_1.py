def co2():
    import pandas as pd
    # 读取 Data 表
    data = pd.read_excel('ClimateChange.xlsx')
    # 取 'Series code' 这列中值为 'EN.ATM.CO2E.KT' 的行并设置索引
    data = data[data['Series code']=='EN.ATM.CO2E.KT'].set_index('Country code')
    # 刪掉多余的前五列，只留各年排量数据
    data.drop(data.columns[:5], axis=1, inplace=True)
    # 把数组中值为 '..' 的元素替换成 'NaN'
    data.replace({'..': pd.np.nan}, inplace=True)
    # 对 NaN 空值进行向前和向后填充
    data = data.fillna(method='ffill', axis=1).fillna(method='bfill', axis=1)
    # 读取 Country 表
    country = pd.read_excel('ClimateChange.xlsx', 'Country') 
    # 设置国家代号为索引，方便合并数据 
    country.index = country['Country code']
    # 合并这俩 Series ：国家总排量和国家收入属于什么群体
    df = pd.concat([data.sum(axis=1), country['Income group']], axis=1)
    # Sum emissions
    a = df.groupby('Income group').sum()
    # 设置列名
    a.columns = ['Sum emissions']
    # 在 df 中加入一列国家名字
    df[2] = country['Country name']
    # 各收入群体中排放量最高的国家和最高排放量
    h = df.sort_values(0, ascending=False).groupby('Income group').head(1).set_index('Income group')
    # 设置列名
    h.columns = ['Highest emissions', 'Highest emission country']
    # 各收入群体中排放量最低的国家和最低排放量
    l = df[df[0]>0].sort_values(0).groupby('Income group').head(1).set_index('Income group')
    # 设置列名
    l.columns = ['Lowest emissions', 'Lowest emission country']
    # 返回全部数据
    return pd.concat([a, h.sort_index(axis=1), l.sort_index(axis=1)], axis=1)
