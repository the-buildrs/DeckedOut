import { useState } from 'react';
import { useHome } from '../../api';
import styles from '/styles/modules/Home.module.scss';

function PromptSection({ submitPrompt, inputType }: any) {
    const [prompt, setPrompt] = useState("");

    function handleChange(e: any) {
        const newPrompt = e.target.value;
        setPrompt(newPrompt);
    }
    const placeholders = {
        "Summary": "Since the very first websites were developed back in...",
        "Prompt": "The evolution of web design."
    };
    const placeholder = inputType == "Summary" ? placeholders.Summary : placeholders.Prompt;


    return (
        <div className={styles.prompt}>
            <input
                type="text"
                value={prompt}
                onChange={handleChange}
                className={styles.promptInput}
                placeholder={placeholder}
            />
            <button className={styles.submitButton} onClick={() => submitPrompt(prompt)}>&gt;</button>
        </div>
    );
}

function InfoSection({ toggleInputs, inputType }: any) {
    return (
        <div className={styles.inputType}>
            <span>Please enter a {inputType.toLowerCase()}</span>
            <span>
                click
                <span onClick={toggleInputs} style={{ color: 'blue', cursor: 'pointer' }}>
                    &nbsp;here&nbsp;
                </span>
                to instead input a&nbsp;
                <span style={{ textDecoration: 'underline' }}>
                    {inputType === "Summary" ? "prompt" : "summary"}
                </span>
                &nbsp;to generate a deck.
            </span>
        </div>
    );
}

function DownloadInfo({ downloadPpxt, resetInfo, pptxInfo }: any) {
    return (
        <div className={styles.downloadInfo} >
            <div>
                <strong>file: </strong>
                {pptxInfo.title}.pptx
            </div>
            <div className={styles.downloadButtons}>
                <button onClick={downloadPpxt}>download</button>
                <button onClick={resetInfo}>reset</button>
            </div>
        </div>
    );
}

function DownloadLoading() {
    return (<div> Loading...(~1-2 Minutes) </div>);
}

function DownloadSection({ downloadPpxt, resetInfo, downloadState, pptxInfo }: any) {
    return (
        <>
            <img src="pptx.png" alt="pptx" className={styles.pptxIcon} />
            <div className={styles.divider} />
            {
                downloadState === 2 ?
                    <DownloadInfo pptxInfo={pptxInfo} downloadPpxt={downloadPpxt} resetInfo={resetInfo} /> :
                    <DownloadLoading />
            }
        </>
    );
}


function Home() {
    const [inputIndex, setInputIndex] = useState(0);
    const inputTypes = ["Prompt", "Summary"];
    function toggleInputs() {
        if (inputIndex === 0) {
            setInputIndex(1);
        } else {
            setInputIndex(0);
        }
    }

    const {
        submitPrompt,
        downloadPpxt,
        resetInfo,
        pptxInfo,
        downloadState,
        errors,
        resetErrors
    } = useHome();

    return (
        <div className="pageContainer" style={{ justifyContent: "center" }}>
            {errors.length ?
                <div className={styles.errorContainer}>
                    <div>ERROR</div>
                    <div>There was an error processing your query on the backend.</div>
                    <div>Please click
                        <a onClick={resetErrors} style={{ cursor: 'pointer', color: "blue" }}> here </a>
                        to try again.</div>
                </div>
                :
                <>
                    <div className={styles.inputContainer} style={{ display: downloadState ? 'none' : 'flex' }}>
                        <PromptSection submitPrompt={submitPrompt} inputType={inputTypes[inputIndex]} />
                        <InfoSection toggleInputs={toggleInputs} inputType={inputTypes[inputIndex]} />
                    </div>

                    <div className={styles.donwloadSection} style={{ display: downloadState ? "flex" : "none" }}>
                        <DownloadSection downloadPpxt={downloadPpxt} resetInfo={resetInfo} pptxInfo={pptxInfo} downloadState={downloadState} />
                    </div>
                </>
            }
        </div>
    );
}

export default Home;