import discord
from discord.ext import commands
import random
import asyncio
import json
import os


class fkkgame(commands.Cog):
    def __init__(self, bot):    
        self.bot = bot
        self.scores_file = "global_points.json" # 🟢 اسم ملف النقاط الموحد والمشترك
        
        # 🟢 التأكد من وجود القفل العام المشترك داخل كائن البوت
        if not hasattr(self.bot, 'global_game_lock'):
            self.bot.global_game_lock = set()

        self.questions = [
            {"image": "فكك_1.png", "answer": "أ س د"},
            {"image": "فكك_2.png", "answer": "ن م ر"},
            {"image": "فكك_3.png", "answer": "ف ه د"},
            {"image": "فكك_4.png", "answer": "ذ ئ ب"},
            {"image": "فكك_5.png", "answer": "ث ع ل ب"},
            {"image": "فكك_6.png", "answer": "د ب"},
            {"image": "فكك_7.png", "answer": "ق ر د"},
            {"image": "فكك_8.png", "answer": "غ و ر ي ل ا"},
            {"image": "فكك_9.png", "answer": "ز ر ا ف ة"},
            {"image": "فكك_10.png", "answer": "ف ي ل"},
            {"image": "فكك_11.png", "answer": "ح ص ا ن"},
            {"image": "فكك_12.png", "answer": "ح م ا ر"},
            {"image": "فكك_13.png", "answer": "غ ز ا ل"},
            {"image": "فكك_14.png", "answer": "ظ ب ي"},
            {"image": "فكك_15.png", "answer": "أ ر ن ب"},
            {"image": "فكك_16.png", "answer": "ك ل ب"},
            {"image": "فكك_17.png", "answer": "ق ط ة"},
            {"image": "فكك_18.png", "answer": "ف أ ر"},
            {"image": "فكك_19.png", "answer": "س ن ج ا ب"},
            {"image": "فكك_20.png", "answer": "ق ن ف ذ"},
            {"image": "فكك_21.png", "answer": "ت م س ا ح"},
            {"image": "فكك_22.png", "answer": "س ل ح ف ا ة"},
            {"image": "فكك_23.png", "answer": "ث ع ب ا ن"},
            {"image": "فكك_24.png", "answer": "س ح ل ي ة"},
            {"image": "فكك_25.png", "answer": "ض ف د ع"},
            {"image": "فكك_26.png", "answer": "س م ك ة"},
            {"image": "فكك_27.png", "answer": "ق ر ش"},
            {"image": "فكك_28.png", "answer": "ح و ت"},
            {"image": "فكك_29.png", "answer": "د ل ف ي ن"},
            {"image": "فكك_30.png", "answer": "أ خ ط ب و ط"},
            {"image": "فكك_31.png", "answer": "ع ق ر ب"},
            {"image": "فكك_32.png", "answer": "ع ن ك ب و ت"},
            {"image": "فكك_33.png", "answer": "ن م ل ة"},
            {"image": "فكك_34.png", "answer": "ن ح ل ة"},
            {"image": "فكك_35.png", "answer": "ف ر ا ش ة"},
            {"image": "فكك_36.png", "answer": "ص ق ر"},
            {"image": "فكك_37.png", "answer": "ن س ر"},
            {"image": "فكك_38.png", "answer": "ب و م ة"},
            {"image": "فكك_39.png", "answer": "غ ر ا ب"},
            {"image": "فكك_40.png", "answer": "ح م ا م ة"},
            {"image": "فكك_41.png", "answer": "ع ص ف و ر"},
            {"image": "فكك_42.png", "answer": "ب ب غ ا ء"},
            {"image": "فكك_43.png", "answer": "ن ع ا م ة"},
            {"image": "فكك_44.png", "answer": "ط ا و و س"},
            {"image": "فكك_45.png", "answer": "د ج ا ج ة"},
            {"image": "فكك_46.png", "answer": "ب ط ة"},
            {"image": "فكك_47.png", "answer": "إ و ز ة"},
            {"image": "فكك_48.png", "answer": "ب ج ع ة"},
            {"image": "فكك_49.png", "answer": "ن و ر س"},
            {"image": "فكك_50.png", "answer": "ب ط ر ي ق"},
            {"image": "فكك_51.png", "answer": "ت ف ا ح"},
            {"image": "فكك_52.png", "answer": "ب ر ت ق ا ل"},
            {"image": "فكك_53.png", "answer": "م و ز"},
            {"image": "فكك_54.png", "answer": "ع ن ب"},
            {"image": "فكك_55.png", "answer": "ف ر ا و ل ة"},
            {"image": "فكك_56.png", "answer": "ب ط ي خ"},
            {"image": "فكك_57.png", "answer": "ش م ا م"},
            {"image": "فكك_58.png", "answer": "خ و خ"},
            {"image": "فكك_59.png", "answer": "م ش م ش"},
            {"image": "فكك_60.png", "answer": "ك ر ز"},
            {"image": "فكك_61.png", "answer": "ت م ر"},
            {"image": "فكك_62.png", "answer": "ت ي ن"},
            {"image": "فكك_63.png", "answer": "ر م ا ن"},
            {"image": "فكك_64.png", "answer": "ك م ث ر ى"},
            {"image": "فكك_65.png", "answer": "ل ي م و ن"},
            {"image": "فكك_66.png", "answer": "م ا ن ج و"},
            {"image": "فكك_67.png", "answer": "أ ن ا ن ا س"},
            {"image": "فكك_68.png", "answer": "ك ي و ي"},
            {"image": "فكك_69.png", "answer": "ت و ت"},
            {"image": "فكك_70.png", "answer": "ج و ز"},
            {"image": "فكك_71.png", "answer": "ط م ا ط م"},
            {"image": "فكك_72.png", "answer": "خ ي ا ر"},
            {"image": "فكك_73.png", "answer": "ب ص ل"},
            {"image": "فكك_74.png", "answer": "ث و م"},
            {"image": "فكك_75.png", "answer": "ب ط ا ط س"},
            {"image": "فكك_76.png", "answer": "ج ز ر"},
            {"image": "فكك_77.png", "answer": "ب ا ذ ن ج ا ن"},
            {"image": "فكك_78.png", "answer": "ك و س ا"},
            {"image": "فكك_79.png", "answer": "ف ل ف ل"},
            {"image": "فكك_80.png", "answer": "خ س"},
            {"image": "فكك_81.png", "answer": "ب ق د و ن س"},
            {"image": "فكك_82.png", "answer": "ن ع ن ا ع"},
            {"image": "فكك_83.png", "answer": "س ب ا ن خ"},
            {"image": "فكك_84.png", "answer": "م ل ف و ف"},
            {"image": "فكك_85.png", "answer": "ق ر ن ب ي ط"},
            {"image": "فكك_86.png", "answer": "ب ر و ك ل ي"},
            {"image": "فكك_87.png", "answer": "ف ا ص و ل ي ا"},
            {"image": "فكك_88.png", "answer": "ب ا ز ل ا ء"},
            {"image": "فكك_89.png", "answer": "ع د س"},
            {"image": "فكك_90.png", "answer": "ح م ص"},
            {"image": "فكك_91.png", "answer": "ف و ل"},
            {"image": "فكك_92.png", "answer": "ق م ح"},
            {"image": "فكك_93.png", "answer": "ذ ر ة"},
            {"image": "فكك_94.png", "answer": "أ ر ز"},
            {"image": "فكك_95.png", "answer": "ش و ف ا ن"},
            {"image": "فكك_96.png", "answer": "ز ي ت و ن"},
            {"image": "فكك_97.png", "answer": "ف ج ل"},
            {"image": "فكك_98.png", "answer": "ك ر ف س"},
            {"image": "فكك_99.png", "answer": "ج ر ج ي ر"},
            {"image": "فكك_100.png", "answer": "ق ر ع"},
            {"image": "فكك_101.png", "answer": "ط ا و ل ة"},
            {"image": "فكك_102.png", "answer": "ك ر س ي"},
            {"image": "فكك_103.png", "answer": "أ ر ي ك ة"},
            {"image": "فكك_104.png", "answer": "س ر ي ر"},
            {"image": "فكك_105.png", "answer": "خ ز ا ن ة"},
            {"image": "فكك_106.png", "answer": "م ر آ ة"},
            {"image": "فكك_107.png", "answer": "س ج ا د ة"},
            {"image": "فكك_108.png", "answer": "س ت ا ر ة"},
            {"image": "فكك_109.png", "answer": "و س ا د ة"},
            {"image": "فكك_110.png", "answer": "ب ط ا ن ي ة"},
            {"image": "فكك_111.png", "answer": "م ص ب ا ح"},
            {"image": "فكك_112.png", "answer": "ث ر ي ا"},
            {"image": "فكك_113.png", "answer": "ش م ع ة"},
            {"image": "فكك_114.png", "answer": "ت ل ف ا ز"},
            {"image": "فكك_115.png", "answer": "م ذ ي ا ع"},
            {"image": "فكك_116.png", "answer": "ح ا س و ب"},
            {"image": "فكك_117.png", "answer": "ه ا ت ف"},
            {"image": "فكك_118.png", "answer": "ط ا ب ع ة"},
            {"image": "فكك_119.png", "answer": "ش ا ش ة"},
            {"image": "فكك_120.png", "answer": "س م ا ع ة"},
            {"image": "فكك_121.png", "answer": "ث ل ا ج ة"},
            {"image": "فكك_122.png", "answer": "غ س ا ل ة"},
            {"image": "فكك_123.png", "answer": "ف ر ن"},
            {"image": "فكك_124.png", "answer": "م ي ك ر و و ي ف"},
            {"image": "فكك_125.png", "answer": "خ ل ا ط"},
            {"image": "فكك_126.png", "answer": "م ك و ا ة"},
            {"image": "فكك_127.png", "answer": "م ك ن س ة"},
            {"image": "فكك_128.png", "answer": "م ر و ح ة"},
            {"image": "فكك_129.png", "answer": "م ك ي ف"},
            {"image": "فكك_130.png", "answer": "س خ ا ن"},
            {"image": "فكك_131.png", "answer": "م ق ص"},
            {"image": "فكك_132.png", "answer": "س ك ي ن"},
            {"image": "فكك_133.png", "answer": "م ل ع ق ة"},
            {"image": "فكك_134.png", "answer": "ش و ك ة"},
            {"image": "فكك_135.png", "answer": "ص ح ن"},
            {"image": "فكك_136.png", "answer": "ك و ب"},
            {"image": "فكك_137.png", "answer": "إ ب ر ي ق"},
            {"image": "فكك_138.png", "answer": "ق د ر"},
            {"image": "فكك_139.png", "answer": "م ق ل ا ة"},
            {"image": "فكك_140.png", "answer": "ز ج ا ج ة"},
            {"image": "فكك_141.png", "answer": "ص ن د و ق"},
            {"image": "فكك_142.png", "answer": "ح ق ي ب ة"},
            {"image": "فكك_143.png", "answer": "م ح ف ظ ة"},
            {"image": "فكك_144.png", "answer": "م ظ ل ة"},
            {"image": "فكك_145.png", "answer": "م ف ت ا ح"},
            {"image": "فكك_146.png", "answer": "ق ف ل"},
            {"image": "فكك_147.png", "answer": "ب ا ب"},
            {"image": "فكك_148.png", "answer": "ن ا ف ذ ة"},
            {"image": "فكك_149.png", "answer": "ج د ا ر"},
            {"image": "فكك_150.png", "answer": "س ق ف"},
            {"image": "فكك_151.png", "answer": "ش ج ر ة"},
            {"image": "فكك_152.png", "answer": "غ ا ب ة"},
            {"image": "فكك_153.png", "answer": "ز ه ر ة"},
            {"image": "فكك_154.png", "answer": "و ر د ة"},
            {"image": "فكك_155.png", "answer": "ع ش ب"},
            {"image": "فكك_156.png", "answer": "ح ج ر"},
            {"image": "فكك_157.png", "answer": "ص خ ر ة"},
            {"image": "فكك_158.png", "answer": "ر م ل"},
            {"image": "فكك_159.png", "answer": "ت ر ا ب"},
            {"image": "فكك_160.png", "answer": "ج ب ل"},
            {"image": "فكك_161.png", "answer": "ت ل"},
            {"image": "فكك_162.png", "answer": "و ا د ي"},
            {"image": "فكك_163.png", "answer": "ص ح ر ا ء"},
            {"image": "فكك_164.png", "answer": "ك ه ف"},
            {"image": "فكك_165.png", "answer": "ب ح ر"},
            {"image": "فكك_166.png", "answer": "م ح ي ط"},
            {"image": "فكك_167.png", "answer": "ن ه ر"},
            {"image": "فكك_168.png", "answer": "ب ح ي ر ة"},
            {"image": "فكك_169.png", "answer": "ش ل ا ل"},
            {"image": "فكك_170.png", "answer": "ب ئ ر"},
            {"image": "فكك_171.png", "answer": "ش ا ط ئ"},
            {"image": "فكك_172.png", "answer": "ج ز ي ر ة"},
            {"image": "فكك_173.png", "answer": "ق ا ر ة"},
            {"image": "فكك_174.png", "answer": "س م ا ء"},
            {"image": "فكك_175.png", "answer": "س ح ا ب"},
            {"image": "فكك_176.png", "answer": "م ط ر"},
            {"image": "فكك_177.png", "answer": "ث ل ج"},
            {"image": "فكك_178.png", "answer": "ب ر ق"},
            {"image": "فكك_179.png", "answer": "ر ع د"},
            {"image": "فكك_180.png", "answer": "ش م س"},
            {"image": "فكك_181.png", "answer": "ق م ر"},
            {"image": "فكك_182.png", "answer": "ن ج م"},
            {"image": "فكك_183.png", "answer": "ك و ك ب"},
            {"image": "فكك_184.png", "answer": "ف ض ا ء"},
            {"image": "فكك_185.png", "answer": "م د ي ن ة"},
            {"image": "فكك_186.png", "answer": "ق ر ي ة"},
            {"image": "فكك_187.png", "answer": "ع ا ص م ة"},
            {"image": "فكك_188.png", "answer": "د و ل ة"},
            {"image": "فكك_189.png", "answer": "م د ر س ة"},
            {"image": "فكك_190.png", "answer": "ج ا م ع ة"},
            {"image": "فكك_191.png", "answer": "م س ت ش ف ى"},
            {"image": "فكك_192.png", "answer": "ص ي د ل ي ة"},
            {"image": "فكك_193.png", "answer": "م س ج د"},
            {"image": "فكك_194.png", "answer": "م ك ت ب ة"},
            {"image": "فكك_195.png", "answer": "م ط ع م"},
            {"image": "فكك_196.png", "answer": "ف ن د ق"},
            {"image": "فكك_197.png", "answer": "ح د ي ق ة"},
            {"image": "فكك_198.png", "answer": "ش ا ر ع"},
            {"image": "فكك_199.png", "answer": "ج س ر"},
            {"image": "فكك_200.png", "answer": "م ط ا ر"},
            {"image": "فكك_201.png", "answer": "ط ب ي ب"},
            {"image": "فكك_202.png", "answer": "م م ر ض"},
            {"image": "فكك_203.png", "answer": "ص ي د ل ي"},
            {"image": "فكك_204.png", "answer": "م ه ن د س"},
            {"image": "فكك_205.png", "answer": "ن ج ا ر"},
            {"image": "فكك_206.png", "answer": "ح د ا د"},
            {"image": "فكك_207.png", "answer": "س ب ا ك"},
            {"image": "فكك_208.png", "answer": "ك ه ر ب ا ئ ي"},
            {"image": "فكك_209.png", "answer": "ب ن ا ء"},
            {"image": "فكك_210.png", "answer": "د ه ا ن"},
            {"image": "فكك_211.png", "answer": "خ ب ا ز"},
            {"image": "فكك_212.png", "answer": "ج ز ا ر"},
            {"image": "فكك_213.png", "answer": "ط ب ا خ"},
            {"image": "فكك_214.png", "answer": "ح ل ا ق"},
            {"image": "فكك_215.png", "answer": "خ ي ا ط"},
            {"image": "فكك_216.png", "answer": "إ س ك ا ف ي"},
            {"image": "فكك_217.png", "answer": "ف ل ا ح"},
            {"image": "فكك_218.png", "answer": "م ز ا ر ع"},
            {"image": "فكك_219.png", "answer": "ص ي ا د"},
            {"image": "فكك_220.png", "answer": "ر ا ع ي"},
            {"image": "فكك_221.png", "answer": "م ع ل م"},
            {"image": "فكك_222.png", "answer": "أ س ت ا ذ"},
            {"image": "فكك_223.png", "answer": "م د ي ر"},
            {"image": "فكك_224.png", "answer": "س ك ر ت ي ر"},
            {"image": "فكك_225.png", "answer": "م ح ا س ب"},
            {"image": "فكك_226.png", "answer": "م ح ا م ي"},
            {"image": "فكك_227.png", "answer": "ق ا ض ي"},
            {"image": "فكك_228.png", "answer": "ش ر ط ي"},
            {"image": "فكك_229.png", "answer": "ج ن د ي"},
            {"image": "فكك_230.png", "answer": "ط ي ا ر"},
            {"image": "فكك_231.png", "answer": "ب ح ا ر"},
            {"image": "فكك_232.png", "answer": "ق ب ط ا ن"},
            {"image": "فكك_233.png", "answer": "س ا ئ ق"},
            {"image": "فكك_234.png", "answer": "م ي ك ا ن ي ك ي"},
            {"image": "فكك_235.png", "answer": "ف ن ا ن"},
            {"image": "فكك_236.png", "answer": "ر س ا م"},
            {"image": "فكك_237.png", "answer": "ن ح ا ت"},
            {"image": "فكك_238.png", "answer": "م م ث ل"},
            {"image": "فكك_239.png", "answer": "م خ ر ج"},
            {"image": "فكك_240.png", "answer": "ك ا ت ب"},
            {"image": "فكك_241.png", "answer": "ش ا ع ر"},
            {"image": "فكك_242.png", "answer": "ص ح ف ي"},
            {"image": "فكك_243.png", "answer": "م ذ ي ع"},
            {"image": "فكك_244.png", "answer": "م ص و ر"},
            {"image": "فكك_245.png", "answer": "ر ي ا ض ي"},
            {"image": "فكك_246.png", "answer": "ل ا ع ب"},
            {"image": "فكك_247.png", "answer": "م د ر ب"},
            {"image": "فكك_248.png", "answer": "ح ك م"},
            {"image": "فكك_249.png", "answer": "ح ا ر س"},
            {"image": "فكك_250.png", "answer": "ر ا ئ د"},
            {"image": "فكك_251.png", "answer": "ر أ س"},
            {"image": "فكك_252.png", "answer": "ش ع ر"},
            {"image": "فكك_253.png", "answer": "و ج ه"},
            {"image": "فكك_254.png", "answer": "ج ب ه ة"},
            {"image": "فكك_255.png", "answer": "ع ي ن"},
            {"image": "فكك_256.png", "answer": "ح ا ج ب"},
            {"image": "فكك_257.png", "answer": "أ ذ ن"},
            {"image": "فكك_258.png", "answer": "أ ن ف"},
            {"image": "فكك_259.png", "answer": "ف م"},
            {"image": "فكك_260.png", "answer": "ش ف ة"},
            {"image": "فكك_261.png", "answer": "س ن"},
            {"image": "فكك_262.png", "answer": "ل س ا ن"},
            {"image": "فكك_263.png", "answer": "خ د"},
            {"image": "فكك_264.png", "answer": "ذ ق ن"},
            {"image": "فكك_265.png", "answer": "ع ن ق"},
            {"image": "فكك_266.png", "answer": "ك ت ف"},
            {"image": "فكك_267.png", "answer": "ظ ه ر"},
            {"image": "فكك_268.png", "answer": "ص د ر"},
            {"image": "فكك_269.png", "answer": "ب ط ن"},
            {"image": "فكك_270.png", "answer": "ذ ر ا ع"},
            {"image": "فكك_271.png", "answer": "ي د"},
            {"image": "فكك_272.png", "answer": "إ ص ب ع"},
            {"image": "فكك_273.png", "answer": "إ ب ه ا م"},
            {"image": "فكك_274.png", "answer": "ظ ف ر"},
            {"image": "فكك_275.png", "answer": "ف خ ذ"},
            {"image": "فكك_276.png", "answer": "ر ك ب ة"},
            {"image": "فكك_277.png", "answer": "س ا ق"},
            {"image": "فكك_278.png", "answer": "ق د م"},
            {"image": "فكك_279.png", "answer": "ك ع ب"},
            {"image": "فكك_280.png", "answer": "ق ل ب"},
            {"image": "فكك_281.png", "answer": "ق م ي ص"},
            {"image": "فكك_282.png", "answer": "ب ن ط ا ل"},
            {"image": "فكك_283.png", "answer": "ف س ت ا ن"},
            {"image": "فكك_284.png", "answer": "ت ن و ر ة"},
            {"image": "فكك_285.png", "answer": "س ت ر ة"},
            {"image": "فكك_286.png", "answer": "م ع ط ف"},
            {"image": "فكك_287.png", "answer": "ع ب ا ء ة"},
            {"image": "فكك_288.png", "answer": "ث و ب"},
            {"image": "فكك_289.png", "answer": "ش م ا غ"},
            {"image": "فكك_290.png", "answer": "ع ق ا ل"},
            {"image": "فكك_291.png", "answer": "ق ب ع ة"},
            {"image": "فكك_292.png", "answer": "ح ذ ا ء"},
            {"image": "فكك_293.png", "answer": "ج و ر ب"},
            {"image": "فكك_294.png", "answer": "ق ف ا ز"},
            {"image": "فكك_295.png", "answer": "و ش ا ح"},
            {"image": "فكك_296.png", "answer": "ح ز ا م"},
            {"image": "فكك_297.png", "answer": "ن ظ ا ر ة"},
            {"image": "فكك_298.png", "answer": "س ا ع ة"},
            {"image": "فكك_299.png", "answer": "خ ا ت م"},
            {"image": "فكك_300.png", "answer": "س و ا ر"}
            ]

    # 🟢 دالة قراءة النقاط وتحديثها في الملف الموحد مباشرة
    def add_score(self, user_id):
        if os.path.exists(self.scores_file):
            with open(self.scores_file, "r", encoding="utf-8") as f:
                try:
                    scores = json.load(f)
                except json.JSONDecodeError:
                    scores = {}
        else:
            scores = {}
        
        user_id_str = str(user_id)
        scores[user_id_str] = scores.get(user_id_str, 0) + 1
        
        with open(self.scores_file, "w", encoding="utf-8") as f:
            json.dump(scores, f, ensure_ascii=False, indent=4)
            
        return scores[user_id_str]

    @commands.command(name="فكك")
    async def start_game_cmd(self, ctx):
        await self.run_game(ctx.channel)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        if message.content.strip() == "فكك":
            await self.run_game(message.channel)

    async def run_game(self, channel):
        # 🟢 الفحص باستخدام القفل العام لمنع تشغيل اللعبة إذا كانت هناك لعبة أخرى نشطة
        if channel.id in self.bot.global_game_lock:
            return await channel.send("⚠️ هناك لعبة جارية بالفعل في هذا الروم! انتظر حتى تنتهي.")

        q = random.choice(self.questions)
        # 🟢 قفل الروم في البوت كاملاً
        self.bot.global_game_lock.add(channel.id)
        
        # 📂 تحديد مسار المجلد الذي يحتوي على الصور
        image_path = os.path.join("images", q["image"])

        # ⚙️ التحقق من أن ملف الصورة موجود فعلياً في المجلد
        if os.path.exists(image_path):
            file = discord.File(image_path, filename=q["image"])
            await channel.send(file=file)
        else:
            await channel.send(f"⚠️ خطأ: لم يتم العثور على ملف الصورة في المسار: `{image_path}`")
            self.bot.global_game_lock.discard(channel.id) # إلغاء القفل عند الخطأ
            return

        def check(m):
            return m.channel == channel and not m.author.bot

        try:
            while True:
                msg = await self.bot.wait_for("message", check=check, timeout=20.0)

                if msg.content.strip() == q["answer"]:
                    # 🟢 تحديث وحفظ النقاط في ملف الجيسون الموحد
                    new_score = self.add_score(msg.author.id)

                    embed = discord.Embed(
                        title="",
                        description=f" {msg.author.mention} فاز في اللعبة!",
                        color=discord.Color.green(),
                    )

                    view = discord.ui.View()
                    
                    # زر النقاط (شفاف/رمادي مع نجمة)
                    score_button = discord.ui.Button(
                        label=f"⋆. 𐙚 ˚  {new_score}",
                        style=discord.ButtonStyle.secondary,
                        disabled=True,
                    )
                    
                

                    # الزر السحري (للدعم)
                    magic_button = discord.ui.Button(
                        label="⋆. 𐙚 ˚",
                        style=discord.ButtonStyle.success # زر أخضر
                    )

                    # الدالة اللي تتنفذ لما ينضغط الزر السحري
                    async def magic_callback(interaction: discord.Interaction):
                        await interaction.response.send_message(
                            "👋 أهلاً بك! هذا سيرفر الدعم الفني الخاص بنا. حياك الله:\nhttps://discord.gg/zkJpxjk2rN", 
                            ephemeral=True # هذي تخلي الرسالة تطلع للي ضغط الزر بس
                        )
                    
                    # ربط الدالة بالزر
                    magic_button.callback = magic_callback

                    # إضافة الأزرار للرسالة
                    view.add_item(score_button)
                    view.add_item(server_button)
                    view.add_item(magic_button)

                    await channel.send(embed=embed, view=view)
                    break 
                else:
                    await msg.add_reaction("❌") 

        except asyncio.TimeoutError:
            await channel.send("⌛ انتهى الوقت! لم يقم أحد بالإجابة الصحيحة.")

        finally:
            # 🟢 فتح القفل العام المشترك فور انتهاء اللعبة
            self.bot.global_game_lock.discard(channel.id)


async def setup(bot):
    await bot.add_cog(fkkgame(bot))