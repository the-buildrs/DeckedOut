import { useEffect, useState } from 'react';
import axios from 'axios';
import { BASE_URL } from '../../context';
import fileDownload from 'js-file-download';

type RequestPayload = { prompt: string };
type PptxInfo = { title: string; data: any };

export default function useHome() {
	const [pptxInfo, setPptxInfo] = useState({
		title: '',
		data: '',
	});
	const [downloadState, setDownloadState] = useState(
		pptxInfo.title.length > 0 ? 2 : 0
	);
	const [errors, setErrors] = useState('');

	useEffect(() => {
		if (pptxInfo.title.length > 0) {
			setDownloadState(2);
		} else {
			setDownloadState(0);
		}
	}, [pptxInfo.title]);

	const mimeType =
		'application/vnd.openxmlformats-officedocument.presentationml.presentation';

	async function submitPrompt(prompt: string) {
		if (prompt.length === 0) return;

		const configs = {
			responseType: 'blob' as any,
			headers: {
				'Access-Control-Allow-Origin': '*',
				'Access-Control-Allow-Credentials': 'true',
				'Access-Control-Allow-Headers':
					'Accept,authorization,Authorization, Content-Type',
				'Access-Control-Allow-Methods':
					'PUT, POST, GET, DELETE, PATCH, OPTIONS',
				'Content-Type': 'application/json',
			},
		};
		const data: RequestPayload = { prompt };
		try {
			setDownloadState(1);
			const res = await axios.post(
				`${BASE_URL}/powerpoint`,
				data,
				configs
			);

			setPptxInfo({
				...pptxInfo,
				title: 'ai-generated-deck',
				data: res.data,
			});
		} catch (error) {
			setErrors(
				'There was an error processing your query on the backend, please try again.'
			);
			console.log(`Received the following error: \n ${error}`);
		}
	}

	function resetInfo() {
		setPptxInfo({
			title: '',
			data: '',
		});
	}

	function resetErrors() {
		setDownloadState(0);
		setErrors('');
	}

	function downloadPpxt() {
		fileDownload(pptxInfo.data, `${pptxInfo.title}.pptx`, mimeType); // TODO: add functionality to add title
	}

	return {
		submitPrompt,
		downloadPpxt,
		resetInfo,
		pptxInfo,
		downloadState,
		errors,
		resetErrors,
	};
}
