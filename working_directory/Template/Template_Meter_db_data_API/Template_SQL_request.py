# Здесь будут хранится sql запросы
# так и живем


# Команды котоыре есть:
# ----------------------------------------------------------------------------------------------------------------------
#                                                 ElectricEnergyValues
# ----------------------------------------------------------------------------------------------------------------------
# Создание временных таблиц для ElectricEnergyValues
ElectricEnergyValues_select_list = \
    [
        """
        SELECT 
        Am AS 'A-0' ,
        Ap AS 'A+0' ,
        Rm AS 'R-0' ,
        Rp AS 'R+0' 
        
        FROM ElectricEnergyValues
        WHERE
        ElectricEnergyValues.Tariff == 0  
        """,
        """
        SELECT 
        Am AS 'A-1' ,
        Ap AS 'A+1' ,
        Rm AS 'R-1' ,
        Rp AS 'R+1' 
        
        FROM ElectricEnergyValues
        WHERE
        ElectricEnergyValues.Tariff == 1  
        """,

        """
        SELECT 
        Am AS 'A-2' ,
        Ap AS 'A+2' ,
        Rm AS 'R-2' ,
        Rp AS 'R+2' 
        
        FROM ElectricEnergyValues
        WHERE
        ElectricEnergyValues.Tariff == 2  
        """,
        """
        SELECT 
        Am AS 'A-3' ,
        Ap AS 'A+3' ,
        Rm AS 'R-3' ,
        Rp AS 'R+3' 
        
        FROM ElectricEnergyValues
        WHERE
        ElectricEnergyValues.Tariff == 3  
        """,
        """
        SELECT 
        Am AS 'A-4' ,
        Ap AS 'A+4' ,
        Rm AS 'R-4' ,
        Rp AS 'R+4' 
        
        FROM ElectricEnergyValues
        WHERE
        ElectricEnergyValues.Tariff == 4  
        """,

    ]

ElectricEnergyValues_create_rate_views = ['''
    CREATE VIEW TARIF0 AS SELECT 
	ElectricEnergyValues.Id,
	ElectricEnergyValues.Am,
	ElectricEnergyValues.Ap,
	ElectricEnergyValues.Rm,
	ElectricEnergyValues.Rp 
	FROM ElectricEnergyValues
	WHERE
		ElectricEnergyValues.Tariff == 0	;''',

                                          '''CREATE VIEW TARIF1 AS
	SELECT 
	ElectricEnergyValues.Id,
	ElectricEnergyValues.Am,
	ElectricEnergyValues.Ap,
	ElectricEnergyValues.Rm,
	ElectricEnergyValues.Rp 
	FROM ElectricEnergyValues
	WHERE
		ElectricEnergyValues.Tariff == 1	;''',

                                          '''CREATE VIEW TARIF2 AS
	SELECT 
	ElectricEnergyValues.Id,
	ElectricEnergyValues.Am,
	ElectricEnergyValues.Ap,
	ElectricEnergyValues.Rm,
	ElectricEnergyValues.Rp 
	FROM ElectricEnergyValues
	WHERE
		ElectricEnergyValues.Tariff == 2	;''',

                                          '''CREATE VIEW TARIF3 AS
	SELECT 
	ElectricEnergyValues.Id,
	ElectricEnergyValues.Am,
	ElectricEnergyValues.Ap,
	ElectricEnergyValues.Rm,
	ElectricEnergyValues.Rp 
	FROM ElectricEnergyValues
	WHERE
		ElectricEnergyValues.Tariff == 3	;''',

                                          '''CREATE VIEW TARIF4 AS
	SELECT 
	ElectricEnergyValues.Id, 
	ElectricEnergyValues.Am,
	ElectricEnergyValues.Ap,
	ElectricEnergyValues.Rm,
	ElectricEnergyValues.Rp 
	FROM ElectricEnergyValues
	WHERE
		ElectricEnergyValues.Tariff == 4	;''']

# Удаление этих временных представлений для ElectricEnergyValues

ElectricEnergyValues_delete_rate_views = ['''DROP VIEW TARIF0 ;''', '''DROP VIEW TARIF1 ;''', '''DROP VIEW TARIF2 ;''',
                                          '''DROP VIEW TARIF3 ;''', '''DROP VIEW TARIF4 ;'''
                                          ]

# Общий селект
ElectricEnergyValues_select = '''
SELECT ArchTypes.Name,	MeterData.DeviceIdx AS id, MeterData.Timestamp AS ts , MeterData.Valid AS Valid,
		TARIF0.Am AS 'A-0' ,
		TARIF0.Ap AS 'A+0' ,
		TARIF0.Rm AS 'R-0' ,
		TARIF0.Rp AS 'R+0' , 

		TARIF1.Am AS 'A-1' ,
		TARIF1.Ap AS 'A+1' ,
		TARIF1.Rm AS 'R-1' ,
		TARIF1.Rp AS 'R+1' ,

		TARIF2.Am AS 'A-2' ,
		TARIF2.Ap AS 'A+2' ,
		TARIF2.Rm AS 'R-2' ,
		TARIF2.Rp AS 'R+2' ,

		TARIF3.Am AS 'A-3' ,
		TARIF3.Ap AS 'A+3' ,
		TARIF3.Rm AS 'R-3' ,
		TARIF3.Rp AS 'R+3' ,

		TARIF4.Am AS 'A-4' ,
		TARIF4.Ap AS 'A+4' ,
		TARIF4.Rm AS 'R-4' ,
		TARIF4.Rp AS 'R+4'

FROM MeterData, ArchTypes , TARIF0 , TARIF1 , TARIF2 , TARIF3 , TARIF4
WHERE
	ArchTypes.Id = MeterData.RecordTypeId AND  
	MeterData.Id = TARIF0.Id AND 
	MeterData.Id = TARIF1.Id AND  
	MeterData.Id = TARIF2.Id AND  
	MeterData.Id = TARIF3.Id AND  
	MeterData.Id = TARIF4.Id
'''

ElectricEnergyValues_insert = """INSERT INTO ElectricEnergyValues (
                                Id,
                                Tariff ,
                                Ap,
                                Rp,
                                Am ,
                                Rm 
                                ) VALUES
                              """

# ----------------------------------------------------------------------------------------------------------------------
#                                                 ElectricConfig
# ----------------------------------------------------------------------------------------------------------------------
# Здесь лежит команда для таблицы ElectricConfig - Только селект
ElectricConfig_Select = '''
SELECT

	DeviceIdx AS id, 
	Timestamp AS ts, 
	Serial AS serial, 
	Model AS model, 
	IntervalPowerArrays AS cArrays, 
	DST AS isDst, 
	Clock AS isClock, 
	Tariff AS isTrf, 
	Reactive AS isAm, 
	ActiveReverse AS isRm, 
	ReactiveReverse AS isRp, 
	CurrentCoeff AS kI, 
	VoltageCoeff AS kU, 
	MeterConst AS const

FROM
	ElectricConfig

WHERE
	DeviceIdx > 0
'''

ElectricConfig_insert = """INSERT INTO ElectricConfig (DeviceIdx, 
                                                                  Timestamp ,
                                                                  Serial , 
                                                                  Model ,
                                                                  IntervalPowerArrays ,
                                                                   DST  ,
                                                                Clock  ,
                                                                Tariff,
                                                                Reactive ,
                                                                ActiveReverse ,
                                                                ReactiveReverse ,
                                                                CurrentCoeff,
                                                                VoltageCoeff,
                                                                MeterConst)
                                                VALUES """

# ----------------------------------------------------------------------------------------------------------------------
#                                               PulseConfig
# ----------------------------------------------------------------------------------------------------------------------
PulseConfig_select = """
SELECT

	DeviceIdx AS id, 
	Timestamp AS ts, 
	Serial AS serial, 
	Model AS model, 
	Channels AS chnl, 
	DST AS isDst

FROM
	PulseConfig

WHERE
	DeviceIdx > 0

"""

PulseConfig_insert = """INSERT INTO    PulseConfig (
                                                        DeviceIdx ,
                                                        Timestamp ,
                                                        Serial  ,
                                                        Model   ,
                                                        Channels,
                                                        DST     
                                                        )
                                                            VALUES """
# ----------------------------------------------------------------------------------------------------------------------
#                                       DigitalConfig
# ----------------------------------------------------------------------------------------------------------------------
DigitalConfig_select = """
SELECT

	DeviceIdx AS id, 
	Timestamp AS ts, 
	Serial AS serial, 
	Model AS model, 
	ChannelsIn AS chnlIn,
	ChannelsOut AS chnlOut,  
	DST AS isDst

FROM
	DigitalConfig

WHERE
	DeviceIdx > 0
"""

DigitalConfig_insert = """INSERT INTO    DigitalConfig (         DeviceIdx ,
                                                                Timestamp,
                                                                Serial   ,
                                                                Model    ,
                                                                ChannelsIn ,
                                                                ChannelsOut ,
                                                                DST   
                                                                 )
                                                VALUES """
# ----------------------------------------------------------------------------------------------------------------------
#                                               ElectricQualityValues
# ----------------------------------------------------------------------------------------------------------------------
# Запросы для ElectricQualityValues
# Создание временных таблиц для ElectricEnergyValues

ElectricQualityValues_create_rate_views = ['''
CREATE VIEW Phase_A AS
	SELECT
	ElectricQualityValues.Id,
	ElectricQualityValues.U,
	ElectricQualityValues.I,
	ElectricQualityValues.P,
	ElectricQualityValues.Q,
	ElectricQualityValues.S,
	ElectricQualityValues.KP,
	ElectricQualityValues.Angle

	FROM
		ElectricQualityValues
	WHERE
		ElectricQualityValues.Phase == 'A'	;
		''',

                                           '''

CREATE VIEW Phase_B AS
	SELECT 
	ElectricQualityValues.Id,
	ElectricQualityValues.U,
	ElectricQualityValues.I,
	ElectricQualityValues.P,
	ElectricQualityValues.Q,
	ElectricQualityValues.S,
	ElectricQualityValues.KP,
	ElectricQualityValues.Angle

	FROM
		ElectricQualityValues
	WHERE
		ElectricQualityValues.Phase == 'B'	;''',

                                           '''
CREATE VIEW Phase_C AS
	SELECT
	ElectricQualityValues.Id,
	ElectricQualityValues.U,
	ElectricQualityValues.I,
	ElectricQualityValues.P,
	ElectricQualityValues.Q,
	ElectricQualityValues.S,
	ElectricQualityValues.KP,
	ElectricQualityValues.Angle

	FROM
		ElectricQualityValues
	WHERE
		ElectricQualityValues.Phase == 'C'	;''',

                                           '''CREATE VIEW Phase_Summ AS
	SELECT 
	ElectricQualityValues.Id,
	ElectricQualityValues.P,
	ElectricQualityValues.Q,
	ElectricQualityValues.S,
	ElectricQualityValues.KP,
	ElectricQualityValues.F

	FROM
		ElectricQualityValues
	WHERE
		ElectricQualityValues.Phase == 'Summ'	;
''']

# Общий селект
ElectricQualityValues_select = '''
SELECT ArchTypes.Name,	MeterData.DeviceIdx AS id, MeterData.Timestamp AS ts, MeterData.Valid AS Valid,

	Phase_A.U AS UA,
	Phase_A.I AS IA ,
	Phase_A.P AS  PA,
	Phase_A.Q AS  QA,
	Phase_A.S AS  SA,
	Phase_A.KP AS  kPA,
	Phase_A.Angle AS AngAB,

	Phase_B.U AS UB,
	Phase_B.I AS  IB,
	Phase_B.P AS  PB,
	Phase_B.Q AS  QB,
	Phase_B.S AS  SB,
	Phase_B.KP AS  kPB,
	Phase_B.Angle AS AngBC,

	Phase_C.U AS UC,
	Phase_C.I AS  IC,
	Phase_C.P AS  PC,
	Phase_C.Q AS  QC,
	Phase_C.S AS  SC,
	Phase_C.KP AS  kPC,
	Phase_C.Angle AS AngAC,

	Phase_Summ.P  AS PS,
	Phase_Summ.Q AS QS,
	Phase_Summ.S AS SS,
	Phase_Summ.KP AS kPS,
	Phase_Summ.F AS Freq


FROM MeterData, ArchTypes , Phase_A , Phase_B , Phase_C , Phase_Summ
WHERE
	ArchTypes.Id = MeterData.RecordTypeId AND  
	MeterData.Id = Phase_A.Id AND 
	MeterData.Id = Phase_B.Id AND 
	MeterData.Id = Phase_C.Id AND 
	MeterData.Id = Phase_Summ.Id
'''
ElectricQualityValues_select_list = \
    [
        """
        SELECT 
        U AS UA,
        I AS IA ,
        P AS  PA,
        Q AS  QA,
        S AS  SA,
        KP AS  kPA,
        Angle AS AngAB

        FROM
        ElectricQualityValues
        
        WHERE
        ElectricQualityValues.Phase == 'A'
        """,

        """
        SELECT
         
        U AS UB,
	    I AS  IB,
	    P AS  PB,
	    Q AS  QB,
	    S AS  SB,
	    KP AS  kPB,
	    Angle AS AngBC

        FROM
        ElectricQualityValues
        
        WHERE
        ElectricQualityValues.Phase == 'B'
        """,

        """
        SELECT 
        U AS UC,
	    I AS  IC,
	    P AS  PC,
	    Q AS  QC,
	    S AS  SC,
	    KP AS  kPC,
	    Angle AS AngAC
        

        FROM
        ElectricQualityValues

        WHERE
        ElectricQualityValues.Phase == 'C'
        """,

        """
        SELECT 
        
        P  AS PS,
	    Q AS QS,
	    S AS SS,
	    KP AS kPS,
	    F AS Freq
        
        FROM
        ElectricQualityValues
        
        WHERE
        ElectricQualityValues.Phase == 'Summ'
        """,

    ]

# Удаление этих временных представлений для ElectricEnergyValues

ElectricQualityValues_delete_rate_views = ['''
DROP VIEW Phase_A ;''',

                                           '''
DROP VIEW Phase_B ;''',

                                           '''
DROP VIEW Phase_C ;''',

                                           '''
DROP VIEW Phase_Summ ;
''']

# Инсерт - Это вааажно
ElectricQualityValues_insert = 'INSERT INTO ElectricQualityValues(Id, Phase, U, I, P, Q, S, KP, Angle, F) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ? )'

# ----------------------------------------------------------------------------------------------------------------------
#                                            ElectricPowerValues
# ----------------------------------------------------------------------------------------------------------------------

ElectricPowerValues_select = """
SELECT ArchTypes.Name,	

	MeterData.DeviceIdx AS id, 
	MeterData.Timestamp AS ts,
	MeterData.Valid AS Valid,

	ElectricPowerValues.Period AS cTime,
	ElectricPowerValues.Pp AS 'P+' ,
	ElectricPowerValues.Pm AS 'P-',
	ElectricPowerValues.Qp AS 'Q+',
	ElectricPowerValues.Qm AS 'Q-',
	ElectricPowerValues.Partial AS isPart,
	ElectricPowerValues.Overflow AS isOvfl ,
	ElectricPowerValues.Season AS isSummer



FROM MeterData, ArchTypes , ElectricPowerValues
WHERE
	ArchTypes.Id = MeterData.RecordTypeId AND 
	ElectricPowerValues.Id = MeterData.Id AND 
	DeviceIdx > 0

"""

ElectricPowerValues_select_list = ["""
SELECT	

	Period AS cTime,
	Pp AS 'P+' ,
	Pm AS 'P-',
	Qp AS 'Q+',
	Qm AS 'Q-',
	Partial AS isPart,
	Overflow AS isOvfl ,
	Season AS isSummer

FROM ElectricPowerValues
WHERE
	Id > 0
"""]

ElectricPowerValues_insert = 'INSERT INTO ElectricPowerValues(Id , Period, Pp, Qp , Pm, Qm ,Partial, Overflow, Season ) VALUES (?, ?,?, ?,?, ?,?, ?, ?)'

# ----------------------------------------------------------------------------------------------------------------------
#                                            PulseValues
# ----------------------------------------------------------------------------------------------------------------------


PulseValues_select = """
SELECT ArchTypes.Name,	
MeterData.DeviceIdx AS id, 
MeterData.Timestamp AS ts,
MeterData.Valid AS Valid,

PulseValues.Channels,
    PulseValues.Chnl1     AS   Pls1    ,
    PulseValues.Chnl2     AS   Pls2    ,
    PulseValues.Chnl3     AS   Pls3    ,
    PulseValues.Chnl4     AS   Pls4    ,
    PulseValues.Chnl5     AS   Pls5    ,
    PulseValues.Chnl6     AS   Pls6    ,
    PulseValues.Chnl7     AS   Pls7    ,
    PulseValues.Chnl8     AS   Pls8    ,
    PulseValues.Chnl9     AS   Pls9    ,
    PulseValues.Chnl10    AS   Pls10    ,
    PulseValues.Chnl11    AS   Pls11    ,
    PulseValues.Chnl12    AS   Pls12    ,
    PulseValues.Chnl13    AS   Pls13    ,
    PulseValues.Chnl14    AS   Pls14    ,
    PulseValues.Chnl15    AS   Pls15    ,
    PulseValues.Chnl16    AS   Pls16    ,
    PulseValues.Chnl17    AS   Pls17    ,
    PulseValues.Chnl18    AS   Pls18    ,
    PulseValues.Chnl19    AS   Pls19    ,
    PulseValues.Chnl20    AS   Pls20    ,
    PulseValues.Chnl21    AS   Pls21    ,
    PulseValues.Chnl22    AS   Pls22    ,
    PulseValues.Chnl23    AS   Pls23    ,
    PulseValues.Chnl24    AS   Pls24    ,
    PulseValues.Chnl25    AS   Pls25    ,
    PulseValues.Chnl26    AS   Pls26    ,
    PulseValues.Chnl27    AS   Pls27    ,
    PulseValues.Chnl28    AS   Pls28    ,
    PulseValues.Chnl29    AS   Pls29    ,
    PulseValues.Chnl30    AS   Pls30    ,
    PulseValues.Chnl31    AS   Pls31    ,
    PulseValues.Chnl32    AS   Pls32

FROM MeterData, ArchTypes , PulseValues
WHERE
	ArchTypes.Id = MeterData.RecordTypeId AND 
	PulseValues.Id = MeterData.Id AND 
	DeviceIdx > 0
"""

PulseValues_select_list = ["""
SELECT 

    Channels ,
    Chnl1     AS   Pls1    ,
    Chnl2     AS   Pls2    ,
    Chnl3     AS   Pls3    ,
    Chnl4     AS   Pls4    ,
    Chnl5     AS   Pls5    ,
    Chnl6     AS   Pls6    ,
    Chnl7     AS   Pls7    ,
    Chnl8     AS   Pls8    ,
    Chnl9     AS   Pls9    ,
    Chnl10    AS   Pls10    ,
    Chnl11    AS   Pls11    ,
    Chnl12    AS   Pls12    ,
    Chnl13    AS   Pls13    ,
    Chnl14    AS   Pls14    ,
    Chnl15    AS   Pls15    ,
    Chnl16    AS   Pls16    ,
    Chnl17    AS   Pls17    ,
    Chnl18    AS   Pls18    ,
    Chnl19    AS   Pls19    ,
    Chnl20    AS   Pls20    ,
    Chnl21    AS   Pls21    ,
    Chnl22    AS   Pls22    ,
    Chnl23    AS   Pls23    ,
    Chnl24    AS   Pls24    ,
    Chnl25    AS   Pls25    ,
    Chnl26    AS   Pls26    ,
    Chnl27    AS   Pls27    ,
    Chnl28    AS   Pls28    ,
    Chnl29    AS   Pls29    ,
    Chnl30    AS   Pls30    ,
    Chnl31    AS   Pls31    ,
    Chnl32    AS   Pls32

FROM  PulseValues
WHERE
	Id  > 0
"""]

PulseValues_insert = 'INSERT INTO PulseValues (Id,Channels,  Chnl1 ,  Chnl2 ,  Chnl3 ,  Chnl4 ,  Chnl5 ,  Chnl6 ,  ' \
                     'Chnl7 ,  Chnl8 ,  Chnl9 ,  Chnl10 ,  Chnl11 ,  Chnl12 ,  Chnl13 ,  Chnl14 ,  Chnl15 ,  Chnl16 , ' \
                     ' Chnl17 ,  Chnl18 ,  Chnl19 ,  Chnl20 ,  Chnl21 ,  Chnl22 ,  Chnl23 ,  Chnl24 ,  Chnl25 ,  ' \
                     'Chnl26 ,  Chnl27 ,  Chnl28 ,  Chnl29 ,  Chnl30 ,  Chnl31 ,  Chnl32) VALUES (? , ? , ? , ? , ? , ' \
                     '? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ' \
                     '? , ? , ? , ? , ?) '
# ----------------------------------------------------------------------------------------------------------------------
#                                   DigitalValues
# ----------------------------------------------------------------------------------------------------------------------
DigitalValues_select = """
SELECT 

ArchTypes.Name,	

MeterData.DeviceIdx AS id, 
MeterData.Timestamp AS ts,
MeterData.Valid AS Valid,

	DigitalValues.Channels,
    DigitalValues.Chnl1            ,
    DigitalValues.Chnl2         ,
    DigitalValues.Chnl3         ,
    DigitalValues.Chnl4         ,
    DigitalValues.Chnl5         ,
    DigitalValues.Chnl6         ,
    DigitalValues.Chnl7         ,
    DigitalValues.Chnl8         ,
    DigitalValues.Chnl9         ,
    DigitalValues.Chnl10        ,
    DigitalValues.Chnl11        ,
    DigitalValues.Chnl12        ,
    DigitalValues.Chnl13        ,
    DigitalValues.Chnl14        ,
    DigitalValues.Chnl15        ,
    DigitalValues.Chnl16        ,
    DigitalValues.Chnl17        ,
    DigitalValues.Chnl18        ,
    DigitalValues.Chnl19        ,
    DigitalValues.Chnl20        ,
    DigitalValues.Chnl21        ,
    DigitalValues.Chnl22        ,
    DigitalValues.Chnl23        ,
    DigitalValues.Chnl24        ,
    DigitalValues.Chnl25        ,
    DigitalValues.Chnl26        ,
    DigitalValues.Chnl27        ,
    DigitalValues.Chnl28        ,
    DigitalValues.Chnl29        ,
    DigitalValues.Chnl30        ,
    DigitalValues.Chnl31        ,
    DigitalValues.Chnl32    




FROM MeterData, ArchTypes , DigitalValues
WHERE
	ArchTypes.Id = MeterData.RecordTypeId AND 
	DigitalValues.Id = MeterData.Id AND 
	DeviceIdx > 0

"""

DigitalValues_select_list = ["""
SELECT 

	Channels       ,
    Chnl1         ,
    Chnl2         ,
    Chnl3         ,
    Chnl4         ,
    Chnl5         ,
    Chnl6         ,
    Chnl7         ,
    Chnl8         ,
    Chnl9         ,
    Chnl10        ,
    Chnl11        ,
    Chnl12        ,
    Chnl13        ,
    Chnl14        ,
    Chnl15        ,
    Chnl16        ,
    Chnl17        ,
    Chnl18        ,
    Chnl19        ,
    Chnl20        ,
    Chnl21        ,
    Chnl22        ,
    Chnl23        ,
    Chnl24        ,
    Chnl25        ,
    Chnl26        ,
    Chnl27        ,
    Chnl28        ,
    Chnl29        ,
    Chnl30        ,
    Chnl31        ,
    Chnl32    




FROM  DigitalValues
WHERE
	Id > 0

"""]

DigitalValues_insert = 'INSERT INTO DigitalValues (Id,Channels,  Chnl1 ,  Chnl2 ,  Chnl3 ,  Chnl4 ,  Chnl5 ,  Chnl6 ,  Chnl7 ,  Chnl8 ,  Chnl9 ,  Chnl10 ,  Chnl11 ,  Chnl12 ,  Chnl13 ,  Chnl14 ,  Chnl15 ,  Chnl16 ,  Chnl17 ,  Chnl18 ,  Chnl19 ,  Chnl20 ,  Chnl21 ,  Chnl22 ,  Chnl23 ,  Chnl24 ,  Chnl25 ,  Chnl26 ,  Chnl27 ,  Chnl28 ,  Chnl29 ,  Chnl30 ,  Chnl31 ,  Chnl32) VALUES (? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ?)'

# ----------------------------------------------------------------------------------------------------------------------
#                                   JournalValues
# ----------------------------------------------------------------------------------------------------------------------


JournalValues_select = """
SELECT 

ArchTypes.Name,	

MeterData.DeviceIdx AS id, 
MeterData.Timestamp AS ts,
MeterData.Valid AS Valid,


    JournalValues.Event     AS  event ,
    JournalValues.EventId    AS eventId




FROM MeterData, ArchTypes , JournalValues
WHERE
	ArchTypes.Id = MeterData.RecordTypeId AND 
	JournalValues.Id = MeterData.Id AND 
	DeviceIdx > 0
"""


JournalValues_select_list = ["""
SELECT 
    Event     AS  event ,
    EventId    AS eventId

FROM  JournalValues
WHERE
	Id  > 0
"""]


JournalValues_insert = """
                        INSERT INTO    JournalValues (          Id ,
                                                                Event,
                                                                EventId  )
                                                VALUES (? , ? , ?)
                        """

# Делаем словарь соответсвия

dictionary_of_correspondences = {

    "DigitalValues":
        {
            "Chnl1": "DigitalValues.Chnl1",
            "Chnl2": "DigitalValues.Chnl2",
            "Chnl3": "DigitalValues.Chnl3",
            "Chnl4": "DigitalValues.Chnl4",
            "Chnl5": "DigitalValues.Chnl5",
            "Chnl6": "DigitalValues.Chnl6",
            "Chnl7": "DigitalValues.Chnl7",
            "Chnl8": "DigitalValues.Chnl8",
            "Chnl9": "DigitalValues.Chnl9",
            "Chnl10": "DigitalValues.Chnl10",
            "Chnl11": "DigitalValues.Chnl11",
            "Chnl12": "DigitalValues.Chnl12",
            "Chnl13": "DigitalValues.Chnl13",
            "Chnl14": "DigitalValues.Chnl14",
            "Chnl15": "DigitalValues.Chnl15",
            "Chnl16": "DigitalValues.Chnl16",
            "Chnl17": "DigitalValues.Chnl17",
            "Chnl18": "DigitalValues.Chnl18",
            "Chnl19": "DigitalValues.Chnl19",
            "Chnl20": "DigitalValues.Chnl20",
            "Chnl21": "DigitalValues.Chnl21",
            "Chnl22": "DigitalValues.Chnl22",
            "Chnl23": "DigitalValues.Chnl23",
            "Chnl24": "DigitalValues.Chnl24",
            "Chnl25": "DigitalValues.Chnl25",
            "Chnl26": "DigitalValues.Chnl26",
            "Chnl27": "DigitalValues.Chnl27",
            "Chnl28": "DigitalValues.Chnl28",
            "Chnl29": "DigitalValues.Chnl29",
            "Chnl30": "DigitalValues.Chnl30",
            "Chnl31": "DigitalValues.Chnl31",
            "Chnl32": "DigitalValues.Chnl32"
        },

    "PulseValues":
        {
            "Pls1": "PulseValues.Chnl1  AS    Pls1",
            "Pls2": "PulseValues.Chnl2  AS    Pls2",
            "Pls3": "PulseValues.Chnl3  AS    Pls3",
            "Pls4": "PulseValues.Chnl4  AS    Pls4",
            "Pls5": "PulseValues.Chnl5  AS    Pls5",
            "Pls6": "PulseValues.Chnl6  AS    Pls6",
            "Pls7": "PulseValues.Chnl7  AS    Pls7",
            "Pls8": "PulseValues.Chnl8  AS    Pls8",
            "Pls9": "PulseValues.Chnl9  AS    Pls9",
            "Pls10": "PulseValues.Chnl10  AS    Pls10",
            "Pls11": "PulseValues.Chnl11  AS    Pls11",
            "Pls12": "PulseValues.Chnl12  AS    Pls12",
            "Pls13": "PulseValues.Chnl13  AS    Pls13",
            "Pls14": "PulseValues.Chnl14  AS    Pls14",
            "Pls15": "PulseValues.Chnl15  AS    Pls15",
            "Pls16": "PulseValues.Chnl16  AS    Pls16",
            "Pls17": "PulseValues.Chnl17  AS    Pls17",
            "Pls18": "PulseValues.Chnl18  AS    Pls18",
            "Pls19": "PulseValues.Chnl19  AS    Pls19",
            "Pls20": "PulseValues.Chnl20  AS    Pls20",
            "Pls21": "PulseValues.Chnl21  AS    Pls21",
            "Pls22": "PulseValues.Chnl22  AS    Pls22",
            "Pls23": "PulseValues.Chnl23  AS    Pls23",
            "Pls24": "PulseValues.Chnl24  AS    Pls24",
            "Pls25": "PulseValues.Chnl25  AS    Pls25",
            "Pls26": "PulseValues.Chnl26  AS    Pls26",
            "Pls27": "PulseValues.Chnl27  AS    Pls27",
            "Pls28": "PulseValues.Chnl28  AS    Pls28",
            "Pls29": "PulseValues.Chnl29  AS    Pls29",
            "Pls30": "PulseValues.Chnl30  AS    Pls30",
            "Pls31": "PulseValues.Chnl31  AS    Pls31",
            "Pls32": "PulseValues.Chnl32  AS    Pls32"
        },

    "ElectricPowerValues":
        {
            "cTime": "ElectricPowerValues.Period AS cTime",
            "P+": "ElectricPowerValues.Pp AS 'P+' ",
            "P-": "ElectricPowerValues.Pm AS 'P-' ",
            "Q+": "ElectricPowerValues.Qp AS 'Q+' ",
            "Q-": "ElectricPowerValues.Qm AS 'Q-' ",
            "isPart": "ElectricPowerValues.Partial AS isPart ",
            "isOvfl": "ElectricPowerValues.Overflow AS isOvfl ",
            "isSummer": "ElectricPowerValues.Season AS isSummer "
        },

    "ElectricQualityValues":
        {
            "UA": "Phase_A.U AS UA",
            "IA": "Phase_A.I AS IA ",
            "PA": "Phase_A.P AS  PA",
            "QA": "Phase_A.Q AS  QA",
            "SA": "Phase_A.S AS  SA",
            "kPA": "Phase_A.KP AS  kPA",
            "AngAB": "Phase_A.Angle AS AngAB",

            "UB": "Phase_B.U AS UB",
            "IB": "Phase_B.I AS  IB",
            "PB": "Phase_B.P AS  PB",
            "QB": "Phase_B.Q AS  QB",
            "SB": "Phase_B.S AS  SB",
            "kPB": "Phase_B.KP AS  kPB",
            "AngBC": "Phase_B.Angle AS AngBC",

            "UC": "Phase_C.U AS UC",
            "IC": "Phase_C.I AS  IC",
            "PC": "Phase_C.P AS  PC",
            "QC": "Phase_C.Q AS  QC",
            "SC": "Phase_C.S AS  SC",
            "kPC": "Phase_C.KP AS  kPC",
            "AngAC": "Phase_C.Angle AS AngAC",

            "PS": "Phase_Summ.P  AS PS",
            "QS": "Phase_Summ.Q AS QS",
            "SS": "Phase_Summ.S AS SS",
            "kPS": "Phase_Summ.KP AS kPS",
            "Freq": "Phase_Summ.F AS Freq"
        },

    "ElectricConfig":
        {
            # "id" : "ElectricConfig.DeviceIdx AS deviceIdx",
            # "ts" : "ElectricConfig.Timestamp AS ts",
            "serial": "ElectricConfig.Serial AS serial",
            "model": "ElectricConfig.Model AS model",
            "cArrays": "ElectricConfig.IntervalPowerArrays AS cArrays",
            "isDst": "ElectricConfig.DST AS isDst",
            "isClock": "ElectricConfig.Clock AS isClock",
            "isTrf": "ElectricConfig.Tariff AS isTrf",
            "isAm": "ElectricConfig.Reactive AS isAm",
            "isRm": "ElectricConfig.ActiveReverse AS isRm",
            "isRp": "ElectricConfig.ReactiveReverse AS isRp",
            "kI": "ElectricConfig.CurrentCoeff AS kI",
            "kU": "ElectricConfig.VoltageCoeff AS kU",
            "const": "ElectricConfig.MeterConst AS const"
        },

    "PulseConfig":

        {
            # "id" : "PulseConfig.DeviceIdx AS deviceIdx",
            # "ts" : "PulseConfig.Timestamp AS ts",
            "serial": "PulseConfig.Serial AS serial",
            "model": "PulseConfig.Model AS model",
            "chnl": "PulseConfig.Channels AS chnl",
            "isDst": "PulseConfig.DST AS isDst"

        },

    "DigitalConfig":
        {
            # "id" : "DigitalConfig.DeviceIdx AS deviceIdx",
            # "ts" : "DigitalConfig.Timestamp AS ts",
            "serial": "DigitalConfig.Serial AS serial",
            "model": "DigitalConfig.Model AS model",
            "chnlIn": "DigitalConfig.ChannelsIn AS chnlIn",
            "chnlOut": "DigitalConfig.ChannelsOut AS chnlOut",
            "isDst": "DigitalConfig.DST AS isDst"
        },

    "ElecticEnergyValues":
        {
            "A-0": "TARIF0.Am AS 'A-0' ",
            "A+0": "TARIF0.Ap AS 'A+0' ",
            "R-0": "TARIF0.Rm AS 'R-0' ",
            "R+0": "TARIF0.Rp AS 'R+0' ",

            "A-1": "TARIF1.Am AS 'A-1' ",
            "A+1": "TARIF1.Ap AS 'A+1' ",
            "R-1": "TARIF1.Rm AS 'R-1' ",
            "R+1": "TARIF1.Rp AS 'R+1' ",

            "A-2": "TARIF2.Am AS 'A-2' ",
            "A+2": "TARIF2.Ap AS 'A+2' ",
            "R-2": "TARIF2.Rm AS 'R-2' ",
            "R+2": "TARIF2.Rp AS 'R+2' ",

            "A-3": "TARIF3.Am AS 'A-3' ",
            "A+3": "TARIF3.Ap AS 'A+3' ",
            "R-3": "TARIF3.Rm AS 'R-3' ",
            "R+3": "TARIF3.Rp AS 'R+3' ",

            "A-4": "TARIF4.Am AS 'A-4' ",
            "A+4": "TARIF4.Ap AS 'A+4' ",
            "R-4": "TARIF4.Rm AS 'R-4' ",
            "R+4": "TARIF4.Rp AS 'R+4' "

        },

    "JournalValues":
        {
            "event": "JournalValues.Event     AS  event",
            "eventId": "JournalValues.EventId    AS eventId"
        }

}
