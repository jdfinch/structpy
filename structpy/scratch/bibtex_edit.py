
bibtex = """

 @inproceedings{Jang_Lee_Park_Lee_Lison_Kim_2019, place={Hong Kong, China}, title={PyOpenDial: A Python-based Domain-Independent Toolkit for Developing Spoken Dialogue Systems with Probabilistic Rules}, url={https://www.aclweb.org/anthology/D19-3032}, DOI={10.18653/v1/D19-3032}, abstractNote={We present PyOpenDial, a Python-based domain-independent, open-source toolkit for spoken dialogue systems. Recent advances in core components of dialogue systems, such as speech recognition, language understanding, dialogue management, and language generation, harness deep learning to achieve state-ofthe-art performance. The original OpenDial, implemented in Java, provides a plugin architecture to integrate external modules, but lacks Python bindings, making it difﬁcult to interface with popular deep learning frameworks such as Tensorﬂow or PyTorch. To this end, we re-implemented OpenDial in Python and extended the toolkit with a number of novel functionalities for neural dialogue state tracking and action planning. We describe the overall architecture and its extensions, and illustrate their use on an example where the system response model is implemented with a recurrent neural network.}, booktitle={Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing and the 9th International Joint Conference on Natural Language Processing (EMNLP-IJCNLP): System Demonstrations}, publisher={Association for Computational Linguistics}, author={Jang, Youngsoo and Lee, Jongmin and Park, Jaeyoung and Lee, Kyeng-Hun and Lison, Pierre and Kim, Kee-Eung}, year={2019}, pages={187–192} }
 
 @article{
     Marietto_de_Aguiar_Barbosa_Botelho_Pimentel_França_daSilva_2013, 
     title={Artificial Intelligence MArkup Language: A Brief Tutorial}, url={http://arxiv.org/abs/1307.3091}, 
     abstractNote={The purpose of this paper is to serve as a reference guide for the development of chatterbots implemented with the AIML language. In order to achieve this, the main concepts in Pattern Recognition area are described because the AIML uses such theoretical framework in their syntactic and semantic structures. After that, AIML language is described and each AIML command/tag is followed by an application example. Also, the usage of AIML embedded tags for the handling of sequence dialogue limitations between humans and machines is shown. Finally, computer systems that assist in the design of chatterbots with the AIML language are classified and described.}, 
     note={arXiv: 1307.3091}, journal={arXiv:1307.3091 [cs]}, 
     author={Marietto, Maria das Graças Bruno and de Aguiar, Rafael Varago and Barbosa, Gislene de Oliveira and Botelho, Wagner Tanaka and Pimentel, Edson and França, Robson dos Santos and da Silva, Vera Lúcia}, 
     year={2013}, 
     month={Jul} 
 }
 
 @inproceedings{Vanzo_Bastianelli_Lemon_2019, place={Stockholm, Sweden}, title={Hierarchical Multi-Task Natural Language Understanding for Cross-domain Conversational AI: HERMIT NLU}, url={https://www.aclweb.org/anthology/W19-5931}, DOI={10.18653/v1/W19-5931}, abstractNote={We present a new neural architecture for widecoverage Natural Language Understanding in Spoken Dialogue Systems. We develop a hierarchical multi-task architecture, which delivers a multi-layer representation of sentence meaning (i.e., Dialogue Acts and Frame-like structures). The architecture is a hierarchy of self-attention mechanisms and BiLSTM encoders followed by CRF tagging layers. We describe a variety of experiments, showing that our approach obtains promising results on a dataset annotated with Dialogue Acts and Frame Semantics. Moreover, we demonstrate its applicability to a different, publicly available NLU dataset annotated with domainspeciﬁc intents and corresponding semantic roles, providing overall performance higher than state-of-the-art tools such as RASA, Dialogﬂow, LUIS, and Watson. For example, we show an average 4.45% improvement in entity tagging F-score over Rasa, Dialogﬂow and LUIS.}, booktitle={Proceedings of the 20th Annual SIGdial Meeting on Discourse and Dialogue}, publisher={Association for Computational Linguistics}, author={Vanzo, Andrea and Bastianelli, Emanuele and Lemon, Oliver}, year={2019}, pages={254–263} }
 
 @inproceedings{Williams_Kamal_Ashour_Amr_Miller_Zweig_2015, place={Prague, Czech Republic}, title={Fast and easy language understanding for dialog systems with Microsoft Language Understanding Intelligent Service (LUIS)}, url={https://www.aclweb.org/anthology/W15-4622}, DOI={10.18653/v1/W15-4622}, booktitle={Proceedings of the 16th Annual Meeting of the Special Interest Group on Discourse and Dialogue}, publisher={Association for Computational Linguistics}, author={Williams, Jason D. and Kamal, Eslam and Ashour, Mokhtar and Amr, Hani and Miller, Jessica and Zweig, Geoff}, year={2015}, month={Sep}, pages={159–161} }
 
@inproceedings{Jang_Lee_Park_Lee_Lison_Kim_2019, place={Hong Kong, China}, title={PyOpenDial: A Python-based Domain-Independent Toolkit for Developing Spoken Dialogue Systems with Probabilistic Rules}, url={https://www.aclweb.org/anthology/D19-3032}, DOI={10.18653/v1/D19-3032}, abstractNote={We present PyOpenDial, a Python-based domain-independent, open-source toolkit for spoken dialogue systems. Recent advances in core components of dialogue systems, such as speech recognition, language understanding, dialogue management, and language generation, harness deep learning to achieve state-ofthe-art performance. The original OpenDial, implemented in Java, provides a plugin architecture to integrate external modules, but lacks Python bindings, making it difﬁcult to interface with popular deep learning frameworks such as Tensorﬂow or PyTorch. To this end, we re-implemented OpenDial in Python and extended the toolkit with a number of novel functionalities for neural dialogue state tracking and action planning. We describe the overall architecture and its extensions, and illustrate their use on an example where the system response model is implemented with a recurrent neural network.}, booktitle={Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing and the 9th International Joint Conference on Natural Language Processing (EMNLP-IJCNLP): System Demonstrations}, publisher={Association for Computational Linguistics}, author={Jang, Youngsoo and Lee, Jongmin and Park, Jaeyoung and Lee, Kyeng-Hun and Lison, Pierre and Kim, Kee-Eung}, year={2019}, pages={187–192} }

 @article{Larsson_Traum_2000, title={{Information state and dialogue management in the TRINDI dialogue move engine toolkit}}, volume={6}, ISSN={13513249}, DOI={10.1017/S1351324900002539}, abstractNote={We introduce an architecture and toolkit for building dialogue managers currently being developed in the TRINDI project, based on the notions of information state and dialogue move engine. The aim is to provide a framework for experimenting with __implementations__ of di erent theories of information state, information state update and dialogue control. A number of dialogue managers are currently being built using the toolkit, and we present a detailed look at one of them. We believe that this framework will make implementation of dialogue processing theories easier, also facilitating comparison of di erent types of dialogue systems, thus helping to achieve a prerequisite for arriving at a best practice for the development of the dialogue management component of a spoken dialogue system.}, number={3 \& 4}, journal={Natural Language Engineering}, author={Larsson, Staffan and Traum, David R.}, year={2000}, month={Sep}, pages={323–340} }

"""


def process_bibtex(bibtex_string):
    for line in bibtex_string.split('\n'):
        i = line.find('title={')
        if i != -1:
            y = None
            for j in range(i, len(line)):
                if line[j] == '}':
                    y = j
                    break
            x = i+len('title={')
            line = line[:x] + '{' + line[x:y] + '}' + line[y:]
        print(line)

if __name__ == '__main__':
    process_bibtex(bibtex)

